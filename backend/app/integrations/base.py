from typing import Optional, Dict, Any
import httpx
from loguru import logger
from app.config import settings

class BaseIntegrationClient:
    """Base client for all integrations"""
    
    def __init__(self, base_url: str, credentials: Optional[Dict] = None):
        self.base_url = base_url
        self.credentials = credentials or {}
        self.headers: Dict[str, str] = {}
        
    async def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        params: Optional[Dict] = None, 
        data: Optional[Dict] = None,
        headers: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """Generic method to make HTTP requests"""
        url = f"{self.base_url}{endpoint}"
        req_headers = {**self.headers, **(headers or {})}
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.request(
                    method, 
                    url, 
                    headers=req_headers, 
                    params=params, 
                    json=data
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                logger.error(f"API Error {self.__class__.__name__}: {e.response.status_code} - {e.response.text}")
                raise
            except Exception as e:
                logger.error(f"Connection Error {self.__class__.__name__}: {str(e)}")
                raise

    async def check_connection(self) -> bool:
        """Abstract method to check connection"""
        raise NotImplementedError
