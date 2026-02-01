from sqlalchemy import Column, String, DateTime, Boolean, Float, Integer, ForeignKey, Enum, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import uuid
import enum

from app.db.session import Base


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"


class User(Base):
    """User model for authentication and profile"""
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    company = Column(String(200), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    # Tenant / Organization
    tenant_id = Column(String(36), nullable=False, index=True)
    
    # Tokens
    verification_token = Column(String(255), nullable=True)
    reset_token = Column(String(255), nullable=True)
    reset_token_expires = Column(DateTime, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    last_login = Column(DateTime, nullable=True)

    # Relationships
    api_keys = relationship("APIKey", back_populates="user", cascade="all, delete-orphan")
    decisions = relationship("Decision", back_populates="user", cascade="all, delete-orphan")
    campaigns = relationship("Campaign", back_populates="user", cascade="all, delete-orphan")


class APIKey(Base):
    """API Key model for programmatic access"""
    __tablename__ = "api_keys"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    key_hash = Column(String(255), nullable=False, unique=True)
    key_prefix = Column(String(12), nullable=False)  # For display
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())
    expires_at = Column(DateTime, nullable=True)
    last_used_at = Column(DateTime, nullable=True)

    # Relationships
    user = relationship("User", back_populates="api_keys")


class Decision(Base):
    """Decision model for storing evaluated strategic decisions"""
    __tablename__ = "decisions"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    tenant_id = Column(String(36), nullable=False, index=True)
    
    # Question and context
    question = Column(Text, nullable=False)
    context = Column(JSON, nullable=True)
    
    # Results
    diagnosis = Column(Text, nullable=True)
    key_metrics = Column(JSON, nullable=True)
    hidden_risks = Column(JSON, nullable=True)
    strategic_principle = Column(Text, nullable=True)
    
    # Scoring
    impact_score = Column(Integer, nullable=True)
    risk_score = Column(Integer, nullable=True)
    urgency_score = Column(Integer, nullable=True)
    mai_score = Column(Float, nullable=True)
    
    # Decisions
    mai_decision = Column(String(20), nullable=True)
    validation_verdict = Column(String(20), nullable=True)
    next_step = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="decisions")


class Campaign(Base):
    """Campaign model for storing ad campaign data"""
    __tablename__ = "campaigns"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    tenant_id = Column(String(36), nullable=False, index=True)
    
    # Campaign info
    external_id = Column(String(255), nullable=False)  # ID from ad platform
    platform = Column(String(50), nullable=False)  # google, meta, linkedin
    name = Column(String(255), nullable=False)
    status = Column(String(20), nullable=False)
    
    # Metrics
    impressions = Column(Integer, default=0)
    clicks = Column(Integer, default=0)
    conversions = Column(Integer, default=0)
    spend = Column(Float, default=0.0)
    revenue = Column(Float, default=0.0)
    
    # Derived metrics (stored for performance)
    ctr = Column(Float, default=0.0)
    cpc = Column(Float, default=0.0)
    cpa = Column(Float, default=0.0)
    roas = Column(Float, default=0.0)
    
    # Date range
    start_date = Column(String(10), nullable=True)  # YYYY-MM-DD
    end_date = Column(String(10), nullable=True)
    
    # Timestamps
    synced_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="campaigns")


class AuditLog(Base):
    """Audit log for tracking important actions"""
    __tablename__ = "audit_logs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), nullable=True)
    tenant_id = Column(String(36), nullable=True, index=True)
    
    # Action details
    action = Column(String(100), nullable=False)  # e.g., "decision.created", "user.login"
    resource_type = Column(String(50), nullable=True)  # e.g., "decision", "campaign"
    resource_id = Column(String(36), nullable=True)
    
    # Context
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(String(500), nullable=True)
    details = Column(JSON, nullable=True)
    
    # Timestamp
    created_at = Column(DateTime, server_default=func.now())
