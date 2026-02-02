from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List, Any
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.integrations import Integration, TenantIntegration

router = APIRouter()

@router.get("/", response_model=List[Any])
async def list_available_integrations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all available integration types (plugins)"""
    result = await db.execute(select(Integration).where(Integration.is_active == True))
    return result.scalars().all()

@router.get("/config", response_model=List[Any])
async def list_tenant_configs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List configurations for the current user's tenant"""
    stmt = (
        select(TenantIntegration)
        .join(Integration)
        .where(TenantIntegration.tenant_id == current_user.tenant_id)
    )
    result = await db.execute(stmt)
    return result.scalars().all()

@router.post("/config")
async def configure_integration(
    integration_id: str,
    credentials: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Configure or update an integration for the tenant"""
    # 1. Check if integration exists
    stmt = select(Integration).where(Integration.id == integration_id)
    result = await db.execute(stmt)
    integration = result.scalar_one_or_none()
    
    if not integration:
        raise HTTPException(status_code=404, detail="Integration type not found")
        
    # 2. Check if config already exists for this tenant
    stmt = select(TenantIntegration).where(
        TenantIntegration.tenant_id == current_user.tenant_id,
        TenantIntegration.integration_id == integration_id
    )
    result = await db.execute(stmt)
    tenant_config = result.scalar_one_or_none()
    
    from app.core.security_encryption import encrypt_string
    import json
    
    # helper for encryption
    credentials_json = json.dumps(credentials)
    encrypted_creds = encrypt_string(credentials_json)
    
    if tenant_config:
        # Update
        tenant_config.credentials_encrypted = encrypted_creds
        tenant_config.is_enabled = True
    else:
        # Create
        tenant_config = TenantIntegration(
            tenant_id=current_user.tenant_id,
            integration_id=integration_id,
            credentials_encrypted=encrypted_creds
        )
        db.add(tenant_config)
        
    await db.commit()
    return {"status": "configured", "integration": integration.name}
