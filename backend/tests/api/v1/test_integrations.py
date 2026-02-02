import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.integrations import Integration

@pytest.mark.asyncio
async def test_list_integrations_empty(client: AsyncClient, normal_user_token: str):
    headers = {"Authorization": f"Bearer {normal_user_token}"}
    response = await client.get("/api/v1/integrations/", headers=headers)
    assert response.status_code == 200
    assert response.json() == []

@pytest.mark.asyncio
async def test_list_integrations_populated(client: AsyncClient, db: AsyncSession, normal_user_token: str):
    # Seed Data
    integration = Integration(
        key="test_service",
        name="Test Service",
        category="test",
        config_schema={"key": "str"}
    )
    db.add(integration)
    await db.commit()
    
    headers = {"Authorization": f"Bearer {normal_user_token}"}
    response = await client.get("/api/v1/integrations/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["key"] == "test_service"

@pytest.mark.asyncio
async def test_configure_integration(client: AsyncClient, db: AsyncSession, normal_user_token: str):
    # Seed Data
    integration = Integration(
        key="google_ads",
        name="Google Ads",
        category="ads",
        config_schema={"client_id": "str"}
    )
    db.add(integration)
    await db.commit()
    
    headers = {"Authorization": f"Bearer {normal_user_token}"}
    payload = {
        "integration_id": integration.id,
        "credentials": {"client_id": "12345"}
    }
    
    # 1. Configure
    response = await client.post("/api/v1/integrations/config", headers=headers, params=payload)
    # Note: Params passed as query in the implementation, but let's check if it should be body or query.
    # Checking implementation: 
    # @router.post("/config")
    # async def configure_integration(integration_id: str, credentials: dict ...
    # FastAPI interprets simple types as Query and Pydantic models/Dict as Body usually, 
    # but since credentials: dict is generic, it might need Body(). 
    # Let's try passing as query for integration_id and body for credentials? 
    # Implementation: `integration_id: str, credentials: dict`
    # Default behavior: integration_id (query), credentials (body)
    
    # Correction: `credentials: dict` in FastAPI often requires Body() or Pydantic model. 
    # If not specified as Body(), FastAPI might expect it as query or break.
    # Let's assume standard behavior: we send integration_id as query, credentials as body.
    
    response = await client.post(
        f"/api/v1/integrations/config?integration_id={integration.id}", 
        headers=headers, 
        json={"client_id": "12345"} # credentials
    )
    
    # Wait, looking at implementation again:
    # async def configure_integration(integration_id: str, credentials: dict, ...)
    # If credentials is just dict, FastAPI might declare it as body. 
    # We will see if tests pass or 422.
    
    assert response.status_code == 200
    assert response.json()["status"] == "configured"
    
    # 2. Verify Config Exists
    response = await client.get("/api/v1/integrations/config", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["integration_id"] == integration.id
    assert data[0]["is_enabled"] == True
