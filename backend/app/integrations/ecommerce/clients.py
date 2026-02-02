from app.integrations.base import BaseIntegrationClient
from app.config import settings

class ShopifyClient(BaseIntegrationClient):
    def __init__(self):
        shop_url = settings.SHOPIFY_SHOP_URL
        super().__init__(f"https://{shop_url}/admin/api/2024-01")
        self.headers = {"X-Shopify-Access-Token": settings.SHOPIFY_ACCESS_TOKEN}
        
    async def check_connection(self) -> bool:
        return bool(settings.SHOPIFY_ACCESS_TOKEN)

class BigCommerceClient(BaseIntegrationClient):
    def __init__(self):
        store_hash = settings.BIGCOMMERCE_STORE_HASH
        super().__init__(f"https://api.bigcommerce.com/stores/{store_hash}/v3")
        self.headers = {"X-Auth-Token": settings.BIGCOMMERCE_ACCESS_TOKEN}
        
    async def check_connection(self) -> bool:
        return bool(settings.BIGCOMMERCE_ACCESS_TOKEN)

class SalesforceCommerceClient(BaseIntegrationClient):
    def __init__(self):
        super().__init__("https://api.commercecloud.salesforce.com")
        
    async def check_connection(self) -> bool:
        return bool(settings.SALESFORCE_CC_CLIENT_ID)
