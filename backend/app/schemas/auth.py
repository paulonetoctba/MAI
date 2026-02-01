from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


# --- Request Schemas ---

class UserRegisterRequest(BaseModel):
    """Schema for user registration"""
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    company: str = Field(..., min_length=2, max_length=200)
    password: str = Field(..., min_length=8, max_length=100)


class UserLoginRequest(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str


class ForgotPasswordRequest(BaseModel):
    """Schema for password reset request"""
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    """Schema for password reset"""
    token: str
    new_password: str = Field(..., min_length=8, max_length=100)


class VerifyEmailRequest(BaseModel):
    """Schema for email verification"""
    token: str


class RefreshTokenRequest(BaseModel):
    """Schema for token refresh"""
    refresh_token: str


# --- Response Schemas ---

class TokenResponse(BaseModel):
    """Schema for token response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class UserResponse(BaseModel):
    """Schema for user response"""
    id: str
    name: str
    email: str
    company: str
    role: str
    is_verified: bool
    created_at: datetime

    class Config:
        from_attributes = True


class MessageResponse(BaseModel):
    """Generic message response"""
    message: str
    success: bool = True
