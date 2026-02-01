from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta
import uuid

from app.db.session import get_db
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
    generate_verification_token,
    generate_reset_token,
)
from app.models.user import User, AuditLog
from app.schemas.auth import (
    UserRegisterRequest,
    UserLoginRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    VerifyEmailRequest,
    RefreshTokenRequest,
    TokenResponse,
    UserResponse,
    MessageResponse,
)
from app.config import settings

router = APIRouter()


@router.post("/register", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def register(
    request: UserRegisterRequest,
    req: Request,
    db: AsyncSession = Depends(get_db),
):
    """Register a new user account"""
    
    # Check if email already exists
    result = await db.execute(
        select(User).where(User.email == request.email)
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    
    # Create tenant ID (company-level isolation)
    tenant_id = str(uuid.uuid4())
    
    # Create user
    user = User(
        id=str(uuid.uuid4()),
        email=request.email,
        name=request.name,
        company=request.company,
        hashed_password=get_password_hash(request.password),
        tenant_id=tenant_id,
        verification_token=generate_verification_token(),
    )
    
    db.add(user)
    
    # Audit log
    audit = AuditLog(
        user_id=user.id,
        tenant_id=tenant_id,
        action="user.registered",
        resource_type="user",
        resource_id=user.id,
        ip_address=req.client.host if req.client else None,
        user_agent=req.headers.get("user-agent"),
    )
    db.add(audit)
    
    await db.commit()
    
    # TODO: Send verification email
    
    return MessageResponse(
        message="Account created successfully. Please check your email to verify your account.",
        success=True,
    )


@router.post("/login", response_model=TokenResponse)
async def login(
    request: UserLoginRequest,
    req: Request,
    db: AsyncSession = Depends(get_db),
):
    """Login and get access token"""
    
    # Find user
    result = await db.execute(
        select(User).where(User.email == request.email)
    )
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is disabled",
        )
    
    # Update last login
    user.last_login = datetime.utcnow()
    
    # Create tokens
    access_token = create_access_token(
        data={"sub": user.id, "email": user.email, "tenant_id": user.tenant_id}
    )
    refresh_token = create_refresh_token(
        data={"sub": user.id}
    )
    
    # Audit log
    audit = AuditLog(
        user_id=user.id,
        tenant_id=user.tenant_id,
        action="user.login",
        resource_type="user",
        resource_id=user.id,
        ip_address=req.client.host if req.client else None,
        user_agent=req.headers.get("user-agent"),
    )
    db.add(audit)
    
    await db.commit()
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


@router.post("/forgot-password", response_model=MessageResponse)
async def forgot_password(
    request: ForgotPasswordRequest,
    db: AsyncSession = Depends(get_db),
):
    """Request password reset email"""
    
    result = await db.execute(
        select(User).where(User.email == request.email)
    )
    user = result.scalar_one_or_none()
    
    if user:
        user.reset_token = generate_reset_token()
        user.reset_token_expires = datetime.utcnow() + timedelta(hours=1)
        await db.commit()
        
        # TODO: Send reset email
    
    # Always return success (security: don't reveal if email exists)
    return MessageResponse(
        message="If an account with that email exists, we sent password reset instructions.",
        success=True,
    )


@router.post("/reset-password", response_model=MessageResponse)
async def reset_password(
    request: ResetPasswordRequest,
    db: AsyncSession = Depends(get_db),
):
    """Reset password with token"""
    
    result = await db.execute(
        select(User).where(
            User.reset_token == request.token,
            User.reset_token_expires > datetime.utcnow(),
        )
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token",
        )
    
    user.hashed_password = get_password_hash(request.new_password)
    user.reset_token = None
    user.reset_token_expires = None
    
    await db.commit()
    
    return MessageResponse(
        message="Password reset successfully. You can now login with your new password.",
        success=True,
    )


@router.post("/verify-email", response_model=MessageResponse)
async def verify_email(
    request: VerifyEmailRequest,
    db: AsyncSession = Depends(get_db),
):
    """Verify email with token"""
    
    result = await db.execute(
        select(User).where(User.verification_token == request.token)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid verification token",
        )
    
    user.is_verified = True
    user.verification_token = None
    
    await db.commit()
    
    return MessageResponse(
        message="Email verified successfully. You can now access all features.",
        success=True,
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    request: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db),
):
    """Refresh access token"""
    
    payload = decode_token(request.refresh_token)
    
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )
    
    user_id = payload.get("sub")
    
    result = await db.execute(
        select(User).where(User.id == user_id, User.is_active == True)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    
    access_token = create_access_token(
        data={"sub": user.id, "email": user.email, "tenant_id": user.tenant_id}
    )
    refresh_token = create_refresh_token(
        data={"sub": user.id}
    )
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


# ============================================
# Social OAuth Endpoints
# ============================================

@router.get("/google")
async def google_auth():
    """Initiate Google OAuth flow"""
    from app.core.oauth import google_oauth
    import secrets
    
    state = secrets.token_urlsafe(32)
    # In production, store state in Redis/session for validation
    
    auth_url = google_oauth.get_authorization_url(state)
    
    return {
        "auth_url": auth_url,
        "state": state,
    }


@router.get("/google/callback")
async def google_callback(
    code: str,
    state: str,
    req: Request,
    db: AsyncSession = Depends(get_db),
):
    """Handle Google OAuth callback"""
    from app.core.oauth import google_oauth
    
    try:
        # Exchange code for tokens
        token_data = await google_oauth.exchange_code(code)
        access_token = token_data.get("access_token")
        
        # Get user info
        user_info = await google_oauth.get_user_info(access_token)
        email = user_info.get("email")
        name = user_info.get("name")
        google_id = user_info.get("id")
        
        # Find or create user
        result = await db.execute(
            select(User).where(User.email == email)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            # Create new user
            tenant_id = str(uuid.uuid4())
            user = User(
                id=str(uuid.uuid4()),
                email=email,
                name=name,
                hashed_password="",  # No password for OAuth users
                tenant_id=tenant_id,
                is_verified=True,  # Email verified by Google
                oauth_provider="google",
                oauth_id=google_id,
            )
            db.add(user)
            
            # Audit log
            audit = AuditLog(
                user_id=user.id,
                tenant_id=tenant_id,
                action="user.registered.oauth",
                resource_type="user",
                resource_id=user.id,
                details={"provider": "google"},
                ip_address=req.client.host if req.client else None,
            )
            db.add(audit)
        
        # Update last login
        user.last_login = datetime.utcnow()
        
        # Create tokens
        access_token = create_access_token(
            data={"sub": user.id, "email": user.email, "tenant_id": user.tenant_id}
        )
        refresh_token = create_refresh_token(
            data={"sub": user.id}
        )
        
        await db.commit()
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"OAuth authentication failed: {str(e)}",
        )


@router.get("/linkedin")
async def linkedin_auth():
    """Initiate LinkedIn OAuth flow"""
    from app.core.oauth import linkedin_oauth
    import secrets
    
    state = secrets.token_urlsafe(32)
    auth_url = linkedin_oauth.get_authorization_url(state)
    
    return {
        "auth_url": auth_url,
        "state": state,
    }


@router.get("/linkedin/callback")
async def linkedin_callback(
    code: str,
    state: str,
    req: Request,
    db: AsyncSession = Depends(get_db),
):
    """Handle LinkedIn OAuth callback"""
    from app.core.oauth import linkedin_oauth
    
    try:
        # Exchange code for tokens
        token_data = await linkedin_oauth.exchange_code(code)
        access_token = token_data.get("access_token")
        
        # Get user info
        user_info = await linkedin_oauth.get_user_info(access_token)
        email = user_info.get("email")
        name = user_info.get("name")
        linkedin_id = user_info.get("sub")
        
        # Find or create user
        result = await db.execute(
            select(User).where(User.email == email)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            # Create new user
            tenant_id = str(uuid.uuid4())
            user = User(
                id=str(uuid.uuid4()),
                email=email,
                name=name,
                hashed_password="",
                tenant_id=tenant_id,
                is_verified=True,
                oauth_provider="linkedin",
                oauth_id=linkedin_id,
            )
            db.add(user)
            
            audit = AuditLog(
                user_id=user.id,
                tenant_id=tenant_id,
                action="user.registered.oauth",
                resource_type="user",
                resource_id=user.id,
                details={"provider": "linkedin"},
                ip_address=req.client.host if req.client else None,
            )
            db.add(audit)
        
        user.last_login = datetime.utcnow()
        
        access_token = create_access_token(
            data={"sub": user.id, "email": user.email, "tenant_id": user.tenant_id}
        )
        refresh_token = create_refresh_token(
            data={"sub": user.id}
        )
        
        await db.commit()
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"OAuth authentication failed: {str(e)}",
        )

