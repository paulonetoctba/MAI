from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


# --- Request Schemas ---

class UserUpdateRequest(BaseModel):
    """Schema for updating user profile"""
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    company: Optional[str] = Field(None, min_length=2, max_length=200)


class ChangePasswordRequest(BaseModel):
    """Schema for changing password"""
    current_password: str
    new_password: str = Field(..., min_length=8, max_length=100)


class CreateAPIKeyRequest(BaseModel):
    """Schema for creating API key"""
    name: str = Field(..., min_length=1, max_length=100)
    expires_in_days: Optional[int] = Field(None, ge=1, le=365)


# --- Response Schemas ---

class UserProfileResponse(BaseModel):
    """Schema for user profile response"""
    id: str
    name: str
    email: str
    company: str
    role: str
    is_verified: bool
    created_at: datetime
    api_keys_count: int = 0

    class Config:
        from_attributes = True


class APIKeyResponse(BaseModel):
    """Schema for API key response"""
    id: str
    name: str
    key_prefix: str  # Only show first 8 chars
    created_at: datetime
    expires_at: Optional[datetime] = None
    is_active: bool = True

    class Config:
        from_attributes = True


class APIKeyCreatedResponse(BaseModel):
    """Schema for newly created API key (shows full key once)"""
    id: str
    name: str
    key: str  # Full key - only shown once
    created_at: datetime
    expires_at: Optional[datetime] = None


class UserListResponse(BaseModel):
    """Schema for list of users (admin only)"""
    users: List[UserProfileResponse]
    total: int
    page: int
    per_page: int
