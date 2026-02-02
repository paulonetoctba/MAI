from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.db.session import Base

class Integration(Base):
    """
    Metadata about available integrations (the 'Plugin' definition).
    e.g. Google Ads, Shopify, VTEX.
    """
    __tablename__ = "integrations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    key = Column(String(50), unique=True, nullable=False, index=True)  # e.g., 'google_ads', 'vtex'
    name = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False)  # ads, ecommerce, crm, etc.
    logo_url = Column(String(500), nullable=True)
    description = Column(Text, nullable=True)
    
    # JSON Schema definition for what fields are required to connect
    # e.g. { "account_id": "string", "api_token": "string" }
    config_schema = Column(JSON, nullable=False, default={})
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    tenant_configs = relationship("TenantIntegration", back_populates="integration")


class TenantIntegration(Base):
    """
    Configuration/Credentials for a specific tenant using an integration.
    """
    __tablename__ = "tenant_integrations"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    tenant_id = Column(String(36), nullable=False, index=True)
    
    integration_id = Column(String(36), ForeignKey("integrations.id", ondelete="CASCADE"), nullable=False)
    
    # Encrypted JSON blob containing the actual API keys/tokens matching config_schema
    credentials_encrypted = Column(Text, nullable=True)
    
    is_enabled = Column(Boolean, default=True)
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    # Relationships
    integration = relationship("Integration", back_populates="tenant_configs")
