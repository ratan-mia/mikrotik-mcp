import asyncio
import time
from datetime import datetime
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Router, RouterMetric, Alert, AlertSeverity
from app.mikrotik_service import get_mikrotik_client
from app.config import get_settings

settings = get_settings()


class MonitoringService:
    """Background service for monitoring routers"""
    
    def __init__(self):
        self.running = False
        self.interval = settings.MONITORING_INTERVAL
    
    async def start(self):
        """Start the monitoring service"""
        self.running = True
        print(f"Monitoring service started (interval: {self.interval}s)")
        
        while self.running:
            try:
                await self.collect_all_metrics()
                await self.check_alerts()
            except Exception as e:
                print(f"Monitoring error: {e}")
            
            await asyncio.sleep(self.interval)
    
    async def stop(self):
        """Stop the monitoring service"""
        self.running = False
        print("Monitoring service stopped")
    
    async def collect_all_metrics(self):
        """Collect metrics from all active routers"""
        db: Session = SessionLocal()
        
        try:
            routers = db.query(Router).filter(Router.is_active == True).all()
            
            for router in routers:
                try:
                    await self.collect_router_metrics(router, db)
                except Exception as e:
                    print(f"Failed to collect metrics for {router.name}: {e}")
            
            db.commit()
        finally:
            db.close()
    
    async def collect_router_metrics(self, router: Router, db: Session):
        """Collect metrics from a single router"""
        try:
            client = get_mikrotik_client(router)
            
            # Get system resources
            system_info = client.get_system_resource()
            connections = client.get_connections()
            
            # Get interface stats
            interfaces = client.get_interfaces()
            total_rx = sum(iface.get('rx_bytes', 0) for iface in interfaces)
            total_tx = sum(iface.get('tx_bytes', 0) for iface in interfaces)
            total_rx_packets = sum(iface.get('rx_packets', 0) for iface in interfaces)
            total_tx_packets = sum(iface.get('tx_packets', 0) for iface in interfaces)
            
            # Create metric record
            metric = RouterMetric(
                router_id=router.id,
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
            
            client.disconnect()
            
            print(f"Collected metrics for {router.name}: CPU={metric.cpu_load}% MEM={metric.memory_used}/{metric.memory_total}MB")
            
        except Exception as e:
            print(f"Error collecting metrics for {router.name}: {e}")
            raise
    
    async def check_alerts(self):
        """Check for alert conditions"""
        db: Session = SessionLocal()
        
        try:
            routers = db.query(Router).filter(Router.is_active == True).all()
            
            for router in routers:
                try:
                    # Get latest metric
                    from sqlalchemy import desc
                    latest_metric = db.query(RouterMetric).filter(
                        RouterMetric.router_id == router.id
                    ).order_by(desc(RouterMetric.timestamp)).first()
                    
                    if not latest_metric:
                        continue
                    
                    # Check CPU threshold
                    if latest_metric.cpu_load and latest_metric.cpu_load > 80:
                        self.create_alert(
                            db,
                            router.id,
                            AlertSeverity.WARNING if latest_metric.cpu_load < 90 else AlertSeverity.CRITICAL,
                            "High CPU Usage",
                            f"CPU usage is at {latest_metric.cpu_load}%"
                        )
                    
                    # Check memory threshold
                    if latest_metric.memory_total:
                        memory_percent = (latest_metric.memory_used / latest_metric.memory_total) * 100
                        if memory_percent > 85:
                            self.create_alert(
                                db,
                                router.id,
                                AlertSeverity.WARNING if memory_percent < 95 else AlertSeverity.CRITICAL,
                                "High Memory Usage",
                                f"Memory usage is at {memory_percent:.1f}%"
                            )
                    
                    # Check connection count
                    if latest_metric.active_connections and latest_metric.active_connections > 5000:
                        self.create_alert(
                            db,
                            router.id,
                            AlertSeverity.WARNING,
                            "High Connection Count",
                            f"Active connections: {latest_metric.active_connections}"
                        )
                
                except Exception as e:
                    print(f"Alert check error for {router.name}: {e}")
            
            db.commit()
        finally:
            db.close()
    
    def create_alert(self, db: Session, router_id: int, severity: AlertSeverity, title: str, message: str):
        """Create an alert if it doesn't already exist"""
        # Check if similar alert already exists in last hour
        from datetime import timedelta
        recent_time = datetime.utcnow() - timedelta(hours=1)
        
        existing = db.query(Alert).filter(
            Alert.router_id == router_id,
            Alert.title == title,
            Alert.created_at >= recent_time,
            Alert.is_acknowledged == False
        ).first()
        
        if not existing:
            alert = Alert(
                router_id=router_id,
                severity=severity,
                title=title,
                message=message
            )
            db.add(alert)
            print(f"Created alert: {title} - {message}")


# Global monitoring instance
monitoring_service = MonitoringService()


async def start_monitoring():
    """Start monitoring in background"""
    await monitoring_service.start()


if __name__ == "__main__":
    # Run monitoring service standalone
    asyncio.run(start_monitoring())
