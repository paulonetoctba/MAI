from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from datetime import datetime, timedelta
import uuid

from app.db.session import get_db
from app.api.deps import get_current_verified_user, get_admin_user
from app.core.security import (
    get_password_hash,
    verify_password,
    generate_api_key,
    hash_api_key,
)
from app.models.user import User, APIKey
from app.schemas.user import (
    UserUpdateRequest,
    ChangePasswordRequest,
    CreateAPIKeyRequest,
    UserProfileResponse,
    APIKeyResponse,
    APIKeyCreatedResponse,
    UserListResponse,
)
from app.schemas.auth import MessageResponse

router = APIRouter()


@router.get("/me", response_model=UserProfileResponse)
async def get_current_user_profile(
    current_user: User = Depends(get_current_verified_user),
    db: AsyncSession = Depends(get_db),
):
    """Get current user profile"""
    
    result = await db.execute(
        select(APIKey).where(APIKey.user_id == current_user.id, APIKey.is_active == True)
    )
    api_keys_count = len(result.scalars().all())
    
    return UserProfileResponse(
        id=current_user.id,
        name=current_user.name,
        email=current_user.email,
        company=current_user.company,
        role=current_user.role.value if hasattr(current_user.role, 'value') else current_user.role,
        is_verified=current_user.is_verified,
        created_at=current_user.created_at,
        api_keys_count=api_keys_count,
    )


@router.put("/me", response_model=UserProfileResponse)
async def update_current_user_profile(
    request: UserUpdateRequest,
    current_user: User = Depends(get_current_verified_user),
    db: AsyncSession = Depends(get_db),
):
    """Update current user profile"""
    
    if request.name:
        current_user.name = request.name
    if request.company:
        current_user.company = request.company
    
    await db.commit()
    await db.refresh(current_user)
    
    return await get_current_user_profile(current_user, db)


@router.post("/me/change-password", response_model=MessageResponse)
async def change_password(
    request: ChangePasswordRequest,
    current_user: User = Depends(get_current_verified_user),
    db: AsyncSession = Depends(get_db),
):
    """Change current user password"""
    
    if not verify_password(request.current_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect",
        )
    
    current_user.hashed_password = get_password_hash(request.new_password)
    await db.commit()
    
    return MessageResponse(message="Password changed successfully")


@router.get("/me/api-keys", response_model=List[APIKeyResponse])
async def list_api_keys(
    current_user: User = Depends(get_current_verified_user),
    db: AsyncSession = Depends(get_db),
):
    """List current user's API keys"""
    
    result = await db.execute(
        select(APIKey)
        .where(APIKey.user_id == current_user.id)
        .order_by(APIKey.created_at.desc())
    )
    api_keys = result.scalars().all()
    
    return [
        APIKeyResponse(
            id=key.id,
            name=key.name,
            key_prefix=key.key_prefix,
            created_at=key.created_at,
            expires_at=key.expires_at,
            is_active=key.is_active,
        )
        for key in api_keys
    ]


@router.post("/me/api-keys", response_model=APIKeyCreatedResponse, status_code=status.HTTP_201_CREATED)
async def create_api_key(
    request: CreateAPIKeyRequest,
    current_user: User = Depends(get_current_verified_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new API key"""
    
    # Generate key
    raw_key = generate_api_key()
    key_prefix = raw_key[:12]
    key_hash = hash_api_key(raw_key)
    
    # Calculate expiration
    expires_at = None
    if request.expires_in_days:
        expires_at = datetime.utcnow() + timedelta(days=request.expires_in_days)
    
    # Create API key record
    api_key = APIKey(
        id=str(uuid.uuid4()),
        user_id=current_user.id,
        name=request.name,
        key_hash=key_hash,
        key_prefix=key_prefix,
        expires_at=expires_at,
    )
    db.add(api_key)
    await db.commit()
    
    return APIKeyCreatedResponse(
        id=api_key.id,
        name=api_key.name,
        key=raw_key,  # Only shown once!
        created_at=api_key.created_at,
        expires_at=api_key.expires_at,
    )


@router.delete("/me/api-keys/{key_id}", response_model=MessageResponse)
async def delete_api_key(
    key_id: str,
    current_user: User = Depends(get_current_verified_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete an API key"""
    
    result = await db.execute(
        select(APIKey).where(
            APIKey.id == key_id,
            APIKey.user_id == current_user.id,
        )
    )
    api_key = result.scalar_one_or_none()
    
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found",
        )
    
    await db.delete(api_key)
    await db.commit()
    
    return MessageResponse(message="API key deleted successfully")


# Admin endpoints

@router.get("/", response_model=UserListResponse)
async def list_users(
    page: int = 1,
    per_page: int = 20,
    admin_user: User = Depends(get_admin_user),
    db: AsyncSession = Depends(get_db),
):
    """List all users (admin only)"""
    
    offset = (page - 1) * per_page
    
    result = await db.execute(
        select(User)
        .where(User.tenant_id == admin_user.tenant_id)
        .order_by(User.created_at.desc())
        .limit(per_page)
        .offset(offset)
    )
    users = result.scalars().all()
    
    # Count total
    count_result = await db.execute(
        select(User).where(User.tenant_id == admin_user.tenant_id)
    )
    total = len(count_result.scalars().all())
    
    return UserListResponse(
        users=[
            UserProfileResponse(
                id=u.id,
                name=u.name,
                email=u.email,
                company=u.company,
                role=u.role.value if hasattr(u.role, 'value') else u.role,
                is_verified=u.is_verified,
                created_at=u.created_at,
            )
            for u in users
        ],
        total=total,
        page=page,
        per_page=per_page,
    )
