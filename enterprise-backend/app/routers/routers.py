from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List
from datetime import datetime
from app.database import get_db
from app.models import Router, RouterMetric, ConnectedDevice, NetworkInterface, User
from app.schemas import (
    RouterCreate,
    RouterUpdate,
    RouterResponse,
    RouterMetricResponse,
    ConnectedDeviceResponse,
    NetworkInterfaceResponse,
    RouterStatus
)
from app.auth import get_current_active_user, require_operator
from app.mikrotik_service import get_mikrotik_client

router = APIRouter(prefix="/routers", tags=["Routers"])


@router.post("/", response_model=RouterResponse, status_code=status.HTTP_201_CREATED)
async def create_router(
    router_data: RouterCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_operator)
):
    """Create a new router"""
    # Check if router name already exists
    existing = db.query(Router).filter(Router.name == router_data.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Router with this name already exists"
        )
    
    db_router = Router(**router_data.dict())
    db.add(db_router)
    db.commit()
    db.refresh(db_router)
    
    return db_router


@router.get("/", response_model=List[RouterResponse])
async def list_routers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """List all routers"""
    routers = db.query(Router).offset(skip).limit(limit).all()
    return routers


@router.get("/{router_id}", response_model=RouterResponse)
async def get_router(
    router_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a specific router"""
    router = db.query(Router).filter(Router.id == router_id).first()
    if not router:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Router not found"
        )
    return router


@router.put("/{router_id}", response_model=RouterResponse)
async def update_router(
    router_id: int,
    router_update: RouterUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_operator)
):
    """Update a router"""
    router = db.query(Router).filter(Router.id == router_id).first()
    if not router:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Router not found"
        )
    
    for field, value in router_update.dict(exclude_unset=True).items():
        if value is not None:
            setattr(router, field, value)
    
    db.commit()
    db.refresh(router)
    
    return router


@router.delete("/{router_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_router(
    router_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_operator)
):
    """Delete a router"""
    router = db.query(Router).filter(Router.id == router_id).first()
    if not router:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Router not found"
        )
    
    db.delete(router)
    db.commit()
    
    return None


@router.get("/{router_id}/status", response_model=RouterStatus)
async def get_router_status(
    router_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get router status with latest metrics"""
    router = db.query(Router).filter(Router.id == router_id).first()
    if not router:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Router not found"
        )
    
    # Get latest metric
    latest_metric = db.query(RouterMetric).filter(
        RouterMetric.router_id == router_id
    ).order_by(desc(RouterMetric.timestamp)).first()
    
    # Get alert count
    from app.models import Alert
    alert_count = db.query(Alert).filter(
        Alert.router_id == router_id,
        Alert.is_acknowledged == False
    ).count()
    
    # Get device count
    device_count = db.query(ConnectedDevice).filter(
        ConnectedDevice.router_id == router_id
    ).count()
    
    return {
        "router": router,
        "latest_metric": latest_metric,
        "alert_count": alert_count,
        "device_count": device_count
    }


@router.post("/{router_id}/collect", response_model=RouterMetricResponse)
async def collect_router_metrics(
    router_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Collect current metrics from router"""
    router = db.query(Router).filter(Router.id == router_id).first()
    if not router:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Router not found"
        )
    
    try:
        client = get_mikrotik_client(router)
        
        # Get system resources
        system_info = client.get_system_resource()
        connections = client.get_connections()
        
        # Get interface stats for total bandwidth
        interfaces = client.get_interfaces()
        total_rx = sum(iface.get('rx_bytes', 0) for iface in interfaces)
        total_tx = sum(iface.get('tx_bytes', 0) for iface in interfaces)
        total_rx_packets = sum(iface.get('rx_packets', 0) for iface in interfaces)
        total_tx_packets = sum(iface.get('tx_packets', 0) for iface in interfaces)
        
        # Create metric record
        metric = RouterMetric(
            router_id=router_id,
            cpu_load=system_info.get('cpu_load', 0),
            memory_used=system_info.get('memory_used', 0),
            memory_total=system_info.get('memory_total', 0),
            active_connections=connections,
            total_rx_bytes=total_rx,
            total_tx_bytes=total_tx,
            total_rx_packets=total_rx_packets,
            total_tx_packets=total_tx_packets
        )
        
        db.add(metric)
        
        # Update router last_seen
        router.last_seen = datetime.utcnow()
        
        db.commit()
        db.refresh(metric)
        
        client.disconnect()
        
        return metric
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to collect metrics: {str(e)}"
        )


@router.get("/{router_id}/devices", response_model=List[ConnectedDeviceResponse])
async def get_router_devices(
    router_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get devices connected to router"""
    router = db.query(Router).filter(Router.id == router_id).first()
    if not router:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Router not found"
        )
    
    try:
        client = get_mikrotik_client(router)
        devices_data = client.get_dhcp_leases()
        client.disconnect()
        
        # Update database
        current_time = datetime.utcnow()
        for device_data in devices_data:
            mac = device_data.get('mac', '')
            if not mac:
                continue
            
            # Find or create device
            device = db.query(ConnectedDevice).filter(
                ConnectedDevice.router_id == router_id,
                ConnectedDevice.mac_address == mac
            ).first()
            
            if device:
                device.ip_address = device_data.get('ip', '')
                device.hostname = device_data.get('hostname', '')
                device.status = device_data.get('status', '')
                device.last_seen = current_time
            else:
                device = ConnectedDevice(
                    router_id=router_id,
                    ip_address=device_data.get('ip', ''),
                    mac_address=mac,
                    hostname=device_data.get('hostname', ''),
                    status=device_data.get('status', ''),
                    first_seen=current_time,
                    last_seen=current_time
                )
                db.add(device)
        
        db.commit()
        
        # Return all devices
        devices = db.query(ConnectedDevice).filter(
            ConnectedDevice.router_id == router_id
        ).all()
        
        return devices
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get devices: {str(e)}"
        )


@router.get("/{router_id}/interfaces", response_model=List[NetworkInterfaceResponse])
async def get_router_interfaces(
    router_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get router network interfaces"""
    router = db.query(Router).filter(Router.id == router_id).first()
    if not router:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Router not found"
        )
    
    try:
        client = get_mikrotik_client(router)
        interfaces_data = client.get_interfaces()
        client.disconnect()
        
        # Update database
        current_time = datetime.utcnow()
        for iface_data in interfaces_data:
            name = iface_data.get('name', '')
            if not name:
                continue
            
            # Find or create interface
            interface = db.query(NetworkInterface).filter(
                NetworkInterface.router_id == router_id,
                NetworkInterface.name == name
            ).first()
            
            if interface:
                interface.running = iface_data.get('running', False)
                interface.rx_bytes = iface_data.get('rx_bytes', 0)
                interface.tx_bytes = iface_data.get('tx_bytes', 0)
                interface.rx_packets = iface_data.get('rx_packets', 0)
                interface.tx_packets = iface_data.get('tx_packets', 0)
                interface.last_updated = current_time
            else:
                interface = NetworkInterface(
                    router_id=router_id,
                    name=name,
                    running=iface_data.get('running', False),
                    rx_bytes=iface_data.get('rx_bytes', 0),
                    tx_bytes=iface_data.get('tx_bytes', 0),
                    rx_packets=iface_data.get('rx_packets', 0),
                    tx_packets=iface_data.get('tx_packets', 0),
                    last_updated=current_time
                )
                db.add(interface)
        
        db.commit()
        
        # Return all interfaces
        interfaces = db.query(NetworkInterface).filter(
            NetworkInterface.router_id == router_id
        ).all()
        
        return interfaces
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get interfaces: {str(e)}"
        )
