from typing import Optional, Dict, List, Any
import httpx
from loguru import logger
from app.config import settings

class VTEXClient:
    """
    Client for interacting with VTEX APIs.
    References:
    - Catalog API: https://developers.vtex.com/docs/api-reference/catalog-api
    - OMS API: https://developers.vtex.com/docs/api-reference/orders-api
    """
    
    def __init__(self):
        self.account_name = settings.VTEX_ACCOUNT_NAME
        self.environment = settings.VTEX_ENVIRONMENT
        self.base_url = f"https://{self.account_name}.{self.environment}.com.br"
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "X-VTEX-API-AppKey": settings.VTEX_APP_KEY,
            "X-VTEX-API-AppToken": settings.VTEX_APP_TOKEN
        }
    
    async def _make_request(self, method: str, endpoint: str, params: Optional[Dict] = None, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Generic method to make HTTP requests to VTEX"""
        url = f"{self.base_url}{endpoint}"
        async with httpx.AsyncClient() as client:
            try:
                response = await client.request(method, url, headers=self.headers, params=params, json=data)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                logger.error(f"VTEX API Error: {e.response.status_code} - {e.response.text}")
                raise
            except Exception as e:
                logger.error(f"VTEX Connection Error: {str(e)}")
                raise

    async def get_product_by_id(self, product_id: str) -> Dict[str, Any]:
        """Get product details by ID"""
        # Catalog API - Get Product by ID
        endpoint = f"/api/catalog/pvt/product/{product_id}"
        return await self._make_request("GET", endpoint)

    async def get_order_by_id(self, order_id: str) -> Dict[str, Any]:
        """Get order details by ID"""
        # OMS API - Get Order
        endpoint = f"/api/oms/pvt/orders/{order_id}"
        return await self._make_request("GET", endpoint)

    async def list_orders(self, page: int = 1, per_page: int = 15) -> Dict[str, Any]:
        """List orders"""
        # OMS API - List Orders
        endpoint = "/api/oms/pvt/orders"
        params = {
            "page": page,
            "per_page": per_page,
            "orderBy": "creationDate,desc"
        }
        return await self._make_request("GET", endpoint, params=params)

    async def check_connection(self) -> bool:
        """Verify if credentials are valid by making a lightweight call"""
        try:
            # Trying to fetch simplified order list as a ping
            await self.list_orders(per_page=1)
            return True
        except Exception:
            return False

vtex_client = VTEXClient()
