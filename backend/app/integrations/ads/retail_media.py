from app.integrations.base import BaseIntegrationClient
from app.config import settings

class AmazonAdsClient(BaseIntegrationClient):
    def __init__(self):
        super().__init__("https://advertising-api.amazon.com")
    
    async def check_connection(self) -> bool:
        return bool(settings.AMAZON_ADS_CLIENT_ID)

class MercadoAdsClient(BaseIntegrationClient):
    def __init__(self):
        super().__init__("https://api.mercadolibre.com")
    
    async def check_connection(self) -> bool:
        return bool(settings.MERCADO_ADS_APP_ID)

class ShopeeAdsClient(BaseIntegrationClient):
    def __init__(self):
        super().__init__("https://partner.shopeemobile.com/api/v1")
    
    async def check_connection(self) -> bool:
        return bool(settings.SHOPEE_ADS_PARTNER_ID)
