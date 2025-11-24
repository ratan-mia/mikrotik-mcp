from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Float, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    OPERATOR = "operator"
    VIEWER = "viewer"


class AlertSeverity(str, enum.Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class BackupStatus(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.VIEWER)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    audit_logs = relationship("AuditLog", back_populates="user")


class Router(Base):
    __tablename__ = "routers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    hostname = Column(String, nullable=False)
    port = Column(Integer, default=22)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)  # Encrypted in production
    description = Column(Text)
    location = Column(String)
    is_active = Column(Boolean, default=True)
    last_seen = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    metrics = relationship("RouterMetric", back_populates="router", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="router", cascade="all, delete-orphan")
    backups = relationship("Backup", back_populates="router", cascade="all, delete-orphan")
    devices = relationship("ConnectedDevice", back_populates="router", cascade="all, delete-orphan")
    interfaces = relationship("NetworkInterface", back_populates="router", cascade="all, delete-orphan")


class RouterMetric(Base):
    __tablename__ = "router_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    router_id = Column(Integer, ForeignKey("routers.id", ondelete="CASCADE"))
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    # System metrics
    cpu_load = Column(Float)
    memory_used = Column(Float)
    memory_total = Column(Float)
    uptime_seconds = Column(Integer)
    active_connections = Column(Integer)
    
    # Network metrics
    total_rx_bytes = Column(Float)
    total_tx_bytes = Column(Float)
    total_rx_packets = Column(Float)
    total_tx_packets = Column(Float)
    
    router = relationship("Router", back_populates="metrics")


class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    router_id = Column(Integer, ForeignKey("routers.id", ondelete="CASCADE"))
    severity = Column(Enum(AlertSeverity), default=AlertSeverity.INFO)
    title = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    is_acknowledged = Column(Boolean, default=False)
    acknowledged_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    acknowledged_at = Column(DateTime(timezone=True))
    
    router = relationship("Router", back_populates="alerts")


class Backup(Base):
    __tablename__ = "backups"
    
    id = Column(Integer, primary_key=True, index=True)
    router_id = Column(Integer, ForeignKey("routers.id", ondelete="CASCADE"))
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_size = Column(Integer)
    status = Column(Enum(BackupStatus), default=BackupStatus.PENDING)
    error_message = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    completed_at = Column(DateTime(timezone=True))
    
    router = relationship("Router", back_populates="backups")


class ConnectedDevice(Base):
    __tablename__ = "connected_devices"
    
    id = Column(Integer, primary_key=True, index=True)
    router_id = Column(Integer, ForeignKey("routers.id", ondelete="CASCADE"))
    ip_address = Column(String, index=True)
    mac_address = Column(String, index=True)
    hostname = Column(String)
    interface = Column(String)
    status = Column(String)
    first_seen = Column(DateTime(timezone=True), server_default=func.now())
    last_seen = Column(DateTime(timezone=True), server_default=func.now())
    
    router = relationship("Router", back_populates="devices")


class NetworkInterface(Base):
    __tablename__ = "network_interfaces"
    
    id = Column(Integer, primary_key=True, index=True)
    router_id = Column(Integer, ForeignKey("routers.id", ondelete="CASCADE"))
    name = Column(String, nullable=False)
    type = Column(String)
    running = Column(Boolean, default=False)
    rx_bytes = Column(Float, default=0)
    tx_bytes = Column(Float, default=0)
    rx_packets = Column(Float, default=0)
    tx_packets = Column(Float, default=0)
    last_updated = Column(DateTime(timezone=True), server_default=func.now())
    
    router = relationship("Router", back_populates="interfaces")


class ScheduledTask(Base):
    __tablename__ = "scheduled_tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    task_type = Column(String, nullable=False)  # backup, script, maintenance
    router_id = Column(Integer, ForeignKey("routers.id", ondelete="CASCADE"), nullable=True)
    schedule_cron = Column(String, nullable=False)  # Cron expression
    command = Column(Text)
    is_active = Column(Boolean, default=True)
    last_run = Column(DateTime(timezone=True))
    next_run = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action = Column(String, nullable=False)
    resource = Column(String)
    details = Column(Text)
    ip_address = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    user = relationship("User", back_populates="audit_logs")
