"""
Tests for authentication endpoints.
"""

import pytest
from httpx import AsyncClient


class TestAuthRegister:
    """Tests for user registration"""
    
    @pytest.mark.asyncio
    async def test_register_success(self, client: AsyncClient):
        """Test successful user registration"""
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "email": "newuser@example.com",
                "name": "New User",
                "password": "SecurePass123!",
                "company": "Test Company",
            },
        )
        
        assert response.status_code == 201
        data = response.json()
        assert data["success"] is True
        assert "Account created" in data["message"]
    
    @pytest.mark.asyncio
    async def test_register_duplicate_email(self, client: AsyncClient, test_user):
        """Test registration with existing email fails"""
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "email": test_user.email,  # Same as existing user
                "name": "Another User",
                "password": "SecurePass123!",
                "company": "Test Company",
            },
        )
        
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"]
    
    @pytest.mark.asyncio
    async def test_register_invalid_email(self, client: AsyncClient):
        """Test registration with invalid email fails"""
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "email": "notanemail",
                "name": "Test User",
                "password": "SecurePass123!",
            },
        )
        
        assert response.status_code == 422  # Validation error


class TestAuthLogin:
    """Tests for user login"""
    
    @pytest.mark.asyncio
    async def test_login_success(self, client: AsyncClient, test_user):
        """Test successful login"""
        response = await client.post(
            "/api/v1/auth/login",
            json={
                "email": test_user.email,
                "password": "testpassword123",
            },
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
    
    @pytest.mark.asyncio
    async def test_login_wrong_password(self, client: AsyncClient, test_user):
        """Test login with wrong password fails"""
        response = await client.post(
            "/api/v1/auth/login",
            json={
                "email": test_user.email,
                "password": "wrongpassword",
            },
        )
        
        assert response.status_code == 401
        assert "Invalid" in response.json()["detail"]
    
    @pytest.mark.asyncio
    async def test_login_nonexistent_user(self, client: AsyncClient):
        """Test login with non-existent user fails"""
        response = await client.post(
            "/api/v1/auth/login",
            json={
                "email": "nonexistent@example.com",
                "password": "anypassword",
            },
        )
        
        assert response.status_code == 401


class TestAuthPasswordReset:
    """Tests for password reset"""
    
    @pytest.mark.asyncio
    async def test_forgot_password(self, client: AsyncClient, test_user):
        """Test forgot password request"""
        response = await client.post(
            "/api/v1/auth/forgot-password",
            json={"email": test_user.email},
        )
        
        assert response.status_code == 200
        # Always returns success for security
        assert response.json()["success"] is True
    
    @pytest.mark.asyncio
    async def test_forgot_password_nonexistent(self, client: AsyncClient):
        """Test forgot password for non-existent email still returns success"""
        response = await client.post(
            "/api/v1/auth/forgot-password",
            json={"email": "nonexistent@example.com"},
        )
        
        # Should still return 200 for security (don't reveal if email exists)
        assert response.status_code == 200


class TestAuthToken:
    """Tests for token operations"""
    
    @pytest.mark.asyncio
    async def test_refresh_token(self, client: AsyncClient, test_user):
        """Test token refresh"""
        # First login to get tokens
        login_response = await client.post(
            "/api/v1/auth/login",
            json={
                "email": test_user.email,
                "password": "testpassword123",
            },
        )
        
        refresh_token = login_response.json()["refresh_token"]
        
        # Refresh the token
        response = await client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": refresh_token},
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
    
    @pytest.mark.asyncio
    async def test_refresh_invalid_token(self, client: AsyncClient):
        """Test refresh with invalid token fails"""
        response = await client.post(
            "/api/v1/auth/refresh",
            json={"refresh_token": "invalid-token"},
        )
        
        assert response.status_code == 401
