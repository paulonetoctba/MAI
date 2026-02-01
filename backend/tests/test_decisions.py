"""
Tests for decision engine and scoring.
"""

import pytest
from httpx import AsyncClient


class TestDecisionEvaluate:
    """Tests for decision evaluation endpoint"""
    
    @pytest.mark.asyncio
    async def test_evaluate_decision_success(self, client: AsyncClient, auth_headers):
        """Test successful decision evaluation"""
        response = await client.post(
            "/api/v1/decisions/evaluate",
            headers=auth_headers,
            json={
                "context": "Aumentar investimento em Google Ads em 50%",
                "category": "paid_media",
                "impact": 8,
                "urgency": 7,
                "risk": 4,
            },
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "decision_id" in data
        assert "score" in data
        assert "recommendation" in data
        assert data["score"] > 0
    
    @pytest.mark.asyncio
    async def test_evaluate_decision_unauthorized(self, client: AsyncClient):
        """Test decision evaluation without auth fails"""
        response = await client.post(
            "/api/v1/decisions/evaluate",
            json={
                "context": "Test decision",
                "category": "paid_media",
            },
        )
        
        assert response.status_code == 401
    
    @pytest.mark.asyncio
    async def test_evaluate_decision_validation(self, client: AsyncClient, auth_headers):
        """Test decision evaluation with invalid data"""
        response = await client.post(
            "/api/v1/decisions/evaluate",
            headers=auth_headers,
            json={
                "context": "",  # Empty context should fail
                "category": "invalid_category",
            },
        )
        
        assert response.status_code == 422


class TestDecisionScore:
    """Tests for MAI Decision Score calculation"""
    
    @pytest.mark.asyncio
    async def test_score_calculation_high(self, client: AsyncClient, auth_headers):
        """Test high score calculation (EXECUTAR)"""
        response = await client.post(
            "/api/v1/decisions/evaluate",
            headers=auth_headers,
            json={
                "context": "Critical marketing optimization",
                "category": "performance",
                "impact": 9,
                "urgency": 8,
                "risk": 2,
            },
        )
        
        assert response.status_code == 200
        data = response.json()
        # High impact * urgency / low risk = high score
        assert data["score"] >= 70
        assert "EXECUTAR" in data["recommendation"].upper() or data["recommendation_action"] == "execute"
    
    @pytest.mark.asyncio
    async def test_score_calculation_medium(self, client: AsyncClient, auth_headers):
        """Test medium score calculation (AJUSTAR)"""
        response = await client.post(
            "/api/v1/decisions/evaluate",
            headers=auth_headers,
            json={
                "context": "Moderate campaign change",
                "category": "performance",
                "impact": 5,
                "urgency": 5,
                "risk": 5,
            },
        )
        
        assert response.status_code == 200
        data = response.json()
        # Medium values = medium score
        assert 30 <= data["score"] <= 70
    
    @pytest.mark.asyncio
    async def test_score_calculation_low(self, client: AsyncClient, auth_headers):
        """Test low score calculation (PAUSAR)"""
        response = await client.post(
            "/api/v1/decisions/evaluate",
            headers=auth_headers,
            json={
                "context": "Risky campaign expansion",
                "category": "performance",
                "impact": 3,
                "urgency": 2,
                "risk": 9,
            },
        )
        
        assert response.status_code == 200
        data = response.json()
        # Low impact * urgency / high risk = low score
        assert data["score"] <= 30


class TestDecisionHistory:
    """Tests for decision history"""
    
    @pytest.mark.asyncio
    async def test_get_decision_history(self, client: AsyncClient, auth_headers):
        """Test fetching decision history"""
        # First create a decision
        await client.post(
            "/api/v1/decisions/evaluate",
            headers=auth_headers,
            json={
                "context": "Test decision for history",
                "category": "paid_media",
            },
        )
        
        # Then fetch history
        response = await client.get(
            "/api/v1/decisions/history",
            headers=auth_headers,
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "decisions" in data
        assert len(data["decisions"]) >= 1
    
    @pytest.mark.asyncio
    async def test_get_decision_by_id(self, client: AsyncClient, auth_headers):
        """Test fetching specific decision"""
        # First create a decision
        create_response = await client.post(
            "/api/v1/decisions/evaluate",
            headers=auth_headers,
            json={
                "context": "Specific decision test",
                "category": "paid_media",
            },
        )
        
        decision_id = create_response.json()["decision_id"]
        
        # Fetch by ID
        response = await client.get(
            f"/api/v1/decisions/{decision_id}",
            headers=auth_headers,
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == decision_id
