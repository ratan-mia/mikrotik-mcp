from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, List
from datetime import datetime
from app.models import UserRole, AlertSeverity, BackupStatus
import re


# User Schemas
class UserBase(BaseModel):
    email: str  # Changed from EmailStr to allow .local domains
    username: str
    full_name: Optional[str] = None
    role: UserRole = UserRole.VIEWER
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str) -> str:
        # Simple email validation that allows .local domains
        if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', v):
            raise ValueError('Invalid email format')
        return v


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    email: Optional[str] = None  # Changed from EmailStr
    username: Optional[str] = None
    full_name: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', v):
            raise ValueError('Invalid email format')
        return v


class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: Optional[datetime] = None
    
    model_config = {"from_attributes": True}


# Auth Schemas
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: Optional[str] = None


# Router Schemas
class RouterBase(BaseModel):
    name: str
    hostname: str
    port: int = 22
    username: str
    description: Optional[str] = None
    location: Optional[str] = None
    is_active: bool = True


class RouterCreate(RouterBase):
    password: str


class RouterUpdate(BaseModel):
    name: Optional[str] = None
    hostname: Optional[str] = None
    port: Optional[int] = None
    username: Optional[str] = None
    password: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    is_active: Optional[bool] = None


class RouterResponse(RouterBase):
    id: int
    last_seen: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True


# Router Metric Schemas
class RouterMetricCreate(BaseModel):
    router_id: int
    cpu_load: Optional[float] = None
    memory_used: Optional[float] = None
    memory_total: Optional[float] = None
    uptime_seconds: Optional[int] = None
    active_connections: Optional[int] = None
    total_rx_bytes: Optional[float] = None
    total_tx_bytes: Optional[float] = None
    total_rx_packets: Optional[float] = None
    total_tx_packets: Optional[float] = None


class RouterMetricResponse(RouterMetricCreate):
    id: int
    timestamp: datetime
    
    class Config:
        from_attributes = True


# Alert Schemas
class AlertCreate(BaseModel):
    router_id: int
    severity: AlertSeverity
    title: str
    message: str


class AlertResponse(AlertCreate):
    id: int
    is_acknowledged: bool
    acknowledged_by: Optional[int]
    created_at: datetime
    acknowledged_at: Optional[datetime]
    
    class Config:
        from_attributes = True


# Backup Schemas
class BackupCreate(BaseModel):
    router_id: int


class BackupResponse(BaseModel):
    id: int
    router_id: int
    filename: str
    file_size: Optional[int]
    status: BackupStatus
    error_message: Optional[str]
    created_at: datetime
    completed_at: Optional[datetime]
    
    class Config:
        from_attributes = True


# Connected Device Schemas
class ConnectedDeviceResponse(BaseModel):
    id: int
    router_id: int
    ip_address: Optional[str]
    mac_address: Optional[str]
    hostname: Optional[str]
    interface: Optional[str]
    status: Optional[str]
    first_seen: datetime
    last_seen: datetime
    
    class Config:
        from_attributes = True


# Network Interface Schemas
class NetworkInterfaceResponse(BaseModel):
    id: int
    router_id: int
    name: str
    type: Optional[str]
    running: bool
    rx_bytes: float
    tx_bytes: float
    rx_packets: float
    tx_packets: float
    last_updated: datetime
    
    class Config:
        from_attributes = True


# Dashboard Schemas
class SystemStats(BaseModel):
    total_routers: int
    active_routers: int
    total_devices: int
    active_alerts: int
    critical_alerts: int


class RouterStatus(BaseModel):
    router: RouterResponse
    latest_metric: Optional[RouterMetricResponse]
    alert_count: int
    device_count: int


# Analytics Schemas
class TimeSeriesData(BaseModel):
    timestamp: datetime
    value: float


class RouterAnalytics(BaseModel):
    router_id: int
    router_name: str
    cpu_usage: List[TimeSeriesData]
    memory_usage: List[TimeSeriesData]
    bandwidth_rx: List[TimeSeriesData]
    bandwidth_tx: List[TimeSeriesData]
    connections: List[TimeSeriesData]
