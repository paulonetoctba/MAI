from functools import wraps
from typing import List, Optional
from fastapi import HTTPException, status

from enum import Enum


class Role(str, Enum):
    """User roles for RBAC"""
    ADMIN = "admin"
    USER = "user"


class Permission(str, Enum):
    """Permissions for granular access control"""
    # User permissions
    READ_OWN_PROFILE = "read:own:profile"
    UPDATE_OWN_PROFILE = "update:own:profile"
    
    # Decision permissions
    CREATE_DECISION = "create:decision"
    READ_DECISIONS = "read:decisions"
    
    # Campaign permissions
    CONNECT_ADS = "connect:ads"
    READ_CAMPAIGNS = "read:campaigns"
    
    # Admin permissions
    MANAGE_USERS = "manage:users"
    VIEW_ALL_DATA = "view:all:data"
    MANAGE_TENANTS = "manage:tenants"


# Role to permissions mapping
ROLE_PERMISSIONS: dict[Role, List[Permission]] = {
    Role.USER: [
        Permission.READ_OWN_PROFILE,
        Permission.UPDATE_OWN_PROFILE,
        Permission.CREATE_DECISION,
        Permission.READ_DECISIONS,
        Permission.CONNECT_ADS,
        Permission.READ_CAMPAIGNS,
    ],
    Role.ADMIN: [
        # Inherits all user permissions
        Permission.READ_OWN_PROFILE,
        Permission.UPDATE_OWN_PROFILE,
        Permission.CREATE_DECISION,
        Permission.READ_DECISIONS,
        Permission.CONNECT_ADS,
        Permission.READ_CAMPAIGNS,
        # Admin-only permissions
        Permission.MANAGE_USERS,
        Permission.VIEW_ALL_DATA,
        Permission.MANAGE_TENANTS,
    ],
}


def has_permission(role: Role, permission: Permission) -> bool:
    """Check if a role has a specific permission"""
    return permission in ROLE_PERMISSIONS.get(role, [])


def get_permissions(role: Role) -> List[Permission]:
    """Get all permissions for a role"""
    return ROLE_PERMISSIONS.get(role, [])


def require_role(required_roles: List[Role]):
    """Decorator to require specific roles for an endpoint"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, current_user=None, **kwargs):
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required",
                )
            
            user_role = Role(current_user.role)
            
            if user_role not in required_roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions",
                )
            
            return await func(*args, current_user=current_user, **kwargs)
        return wrapper
    return decorator


def require_permission(required_permissions: List[Permission]):
    """Decorator to require specific permissions for an endpoint"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, current_user=None, **kwargs):
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required",
                )
            
            user_role = Role(current_user.role)
            user_permissions = get_permissions(user_role)
            
            for permission in required_permissions:
                if permission not in user_permissions:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"Missing permission: {permission.value}",
                    )
            
            return await func(*args, current_user=current_user, **kwargs)
        return wrapper
    return decorator


def check_tenant_access(user_tenant_id: str, resource_tenant_id: str) -> bool:
    """Check if user has access to a resource based on tenant"""
    return user_tenant_id == resource_tenant_id
