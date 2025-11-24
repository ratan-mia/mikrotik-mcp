from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from typing import List
from datetime import datetime, timedelta
from app.database import get_db
from app.models import Router, RouterMetric, Alert, User
from app.schemas import (
    SystemStats,
    RouterAnalytics,
    TimeSeriesData,
    AlertResponse,
    RouterMetricResponse
)
from app.auth import get_current_active_user

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/dashboard", response_model=SystemStats)
async def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get overall system statistics for dashboard"""
    total_routers = db.query(Router).count()
    active_routers = db.query(Router).filter(Router.is_active == True).count()
    
    from app.models import ConnectedDevice
    total_devices = db.query(ConnectedDevice).count()
    
    active_alerts = db.query(Alert).filter(Alert.is_acknowledged == False).count()
    critical_alerts = db.query(Alert).filter(
        Alert.is_acknowledged == False,
        Alert.severity == "critical"
    ).count()
    
    return {
        "total_routers": total_routers,
        "active_routers": active_routers,
        "total_devices": total_devices,
        "active_alerts": active_alerts,
        "critical_alerts": critical_alerts
    }


@router.get("/routers/{router_id}/history", response_model=RouterAnalytics)
async def get_router_analytics(
    router_id: int,
    hours: int = Query(default=24, ge=1, le=168),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get historical analytics for a router"""
    router = db.query(Router).filter(Router.id == router_id).first()
    if not router:
        raise HTTPException(status_code=404, detail="Router not found")
    
    # Get metrics from the last N hours
    since = datetime.utcnow() - timedelta(hours=hours)
    metrics = db.query(RouterMetric).filter(
        RouterMetric.router_id == router_id,
        RouterMetric.timestamp >= since
    ).order_by(RouterMetric.timestamp).all()
    
    # Convert to time series data
    cpu_usage = [
        TimeSeriesData(timestamp=m.timestamp, value=m.cpu_load or 0)
        for m in metrics
    ]
    
    memory_usage = [
        TimeSeriesData(
            timestamp=m.timestamp,
            value=(m.memory_used / m.memory_total * 100) if m.memory_total else 0
        )
        for m in metrics
    ]
    
    bandwidth_rx = [
        TimeSeriesData(timestamp=m.timestamp, value=m.total_rx_bytes or 0)
        for m in metrics
    ]
    
    bandwidth_tx = [
        TimeSeriesData(timestamp=m.timestamp, value=m.total_tx_bytes or 0)
        for m in metrics
    ]
    
    connections = [
        TimeSeriesData(timestamp=m.timestamp, value=m.active_connections or 0)
        for m in metrics
    ]
    
    return {
        "router_id": router_id,
        "router_name": router.name,
        "cpu_usage": cpu_usage,
        "memory_usage": memory_usage,
        "bandwidth_rx": bandwidth_rx,
        "bandwidth_tx": bandwidth_tx,
        "connections": connections
    }


@router.get("/metrics/latest")
async def get_latest_metrics(
    limit: int = Query(default=100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get latest metrics for all routers"""
    # Subquery to get latest metric per router
    subq = db.query(
        RouterMetric.router_id,
        func.max(RouterMetric.timestamp).label('max_timestamp')
    ).group_by(RouterMetric.router_id).subquery()
    
    metrics = db.query(RouterMetric).join(
        subq,
        (RouterMetric.router_id == subq.c.router_id) &
        (RouterMetric.timestamp == subq.c.max_timestamp)
    ).limit(limit).all()
    
    return metrics
