from typing import Dict, Any, Optional
from app.integrations.base import BaseIntegrationClient
from app.config import settings

class SemrushClient(BaseIntegrationClient):
    """
    Client for SEMrush API.
    """
    def __init__(self, credentials: Optional[Dict] = None):
        super().__init__("https://api.semrush.com", credentials)
        # Priority: Dynamic Config > Env Var
        self.api_key = self.credentials.get("api_key") or settings.SEMRUSH_API_KEY

    async def check_connection(self) -> bool:
        """
        Check if API key is valid by making a lightweight request.
        """
        if not self.api_key:
            return False
            
        # Example: Check API units balance
        params = {
            "key": self.api_key,
            "type": "api_units"
        }
        try:
            # SEMrush returns plain text usually, but we check for success status
            # Note: SEMrush API endpoint structure is often just /?key=...
            # We'll use the base _make_request but might need adjustment for text response if base expects JSON.
            # Base client expects JSON. We might need to override _make_request or handle specific endpoint.
            # For this simplified implementation, we assume standard behavior or adapt.
            
            # Actually SEMrush often returns text/csv. Let's handle a simple requests check in a real scenario.
            # Here we will just try to hit the endpoint.
            
            # Re-implementing specific call to avoid JSON parsing error if response is text
            import httpx
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}", params=params)
                return response.status_code == 200
        except Exception:
            return False

    async def domain_overview(self, domain: str, db: str = "us") -> Dict[str, Any]:
        """
        Get domain overview data.
        """
        params = {
            "type": "domain_ranks",
            "key": self.api_key,
            "domain": domain,
            "database": db,
            "export_columns": "Dn,Rk,Or,Ot,Oc,Ad,At,Ac" 
        }
        # This returns text line. Need to parse. 
        # For this example, we keep it simple or assume we want JSON if available (SEMrush is mostly CSV-like).
        # We will wrap the result.
        
        # NOTE: Real SEMrush parsing is complex line-by-line. 
        # Returning raw response for now or implementing a simple parser would be needed.
        pass
