"""
Tests for campaign synchronization endpoints.
"""

import pytest
from httpx import AsyncClient


class TestCampaignSync:
    """Tests for campaign sync operations"""
    
    @pytest.mark.asyncio
    async def test_sync_google_ads(self, client: AsyncClient, auth_headers):
        """Test Google Ads sync"""
        response = await client.post(
            "/api/v1/campaigns/sync/google",
            headers=auth_headers,
            json={
                "start_date": "2024-01-01",
                "end_date": "2024-01-31",
            },
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "Successfully synced" in data["message"]
    
    @pytest.mark.asyncio
    async def test_sync_meta_ads(self, client: AsyncClient, auth_headers):
        """Test Meta Ads sync"""
        response = await client.post(
            "/api/v1/campaigns/sync/meta",
            headers=auth_headers,
            json={
                "start_date": "2024-01-01",
                "end_date": "2024-01-31",
            },
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "Successfully synced" in data["message"]
    
    @pytest.mark.asyncio
    async def test_sync_tiktok_ads(self, client: AsyncClient, auth_headers):
        """Test TikTok Ads sync"""
        response = await client.post(
            "/api/v1/campaigns/sync/tiktok",
            headers=auth_headers,
            json={
                "start_date": "2024-01-01",
                "end_date": "2024-01-31",
            },
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "Successfully synced" in data["message"]
    
    @pytest.mark.asyncio
    async def test_sync_unauthorized(self, client: AsyncClient):
        """Test sync without auth fails"""
        response = await client.post(
            "/api/v1/campaigns/sync/google",
            json={
                "start_date": "2024-01-01",
                "end_date": "2024-01-31",
            },
        )
        
        assert response.status_code == 401


class TestCampaignList:
    """Tests for campaign listing"""
    
    @pytest.mark.asyncio
    async def test_list_campaigns_empty(self, client: AsyncClient, auth_headers):
        """Test listing campaigns when none exist"""
        response = await client.get(
            "/api/v1/campaigns/",
            headers=auth_headers,
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "campaigns" in data
        assert "total" in data
    
    @pytest.mark.asyncio
    async def test_list_campaigns_with_filter(self, client: AsyncClient, auth_headers):
        """Test filtering campaigns by platform"""
        # First sync campaigns
        await client.post(
            "/api/v1/campaigns/sync/google",
            headers=auth_headers,
            json={
                "start_date": "2024-01-01",
                "end_date": "2024-01-31",
            },
        )
        
        # Then filter
        response = await client.get(
            "/api/v1/campaigns/?platform=google",
            headers=auth_headers,
        )
        
        assert response.status_code == 200
        data = response.json()
        for campaign in data["campaigns"]:
            assert campaign["platform"] == "google"


class TestCampaignAggregate:
    """Tests for campaign aggregation"""
    
    @pytest.mark.asyncio
    async def test_get_aggregates_empty(self, client: AsyncClient, auth_headers):
        """Test aggregates when no campaigns exist"""
        response = await client.get(
            "/api/v1/campaigns/aggregate",
            headers=auth_headers,
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["total_spend"] == 0
        assert data["total_revenue"] == 0
    
    @pytest.mark.asyncio
    async def test_get_aggregates_with_data(self, client: AsyncClient, auth_headers):
        """Test aggregates with synced campaigns"""
        # Sync campaigns first
        await client.post(
            "/api/v1/campaigns/sync/google",
            headers=auth_headers,
            json={
                "start_date": "2024-01-01",
                "end_date": "2024-01-31",
            },
        )
        
        response = await client.get(
            "/api/v1/campaigns/aggregate",
            headers=auth_headers,
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["total_spend"] > 0
        assert "by_platform" in data


class TestAdAccounts:
    """Tests for ad account listing"""
    
    @pytest.mark.asyncio
    async def test_list_ad_accounts(self, client: AsyncClient, auth_headers):
        """Test listing connected ad accounts"""
        response = await client.get(
            "/api/v1/campaigns/accounts",
            headers=auth_headers,
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 3  # Google, Meta, TikTok
        platforms = [account["platform"] for account in data]
        assert "google" in platforms
        assert "meta" in platforms
        assert "tiktok" in platforms
