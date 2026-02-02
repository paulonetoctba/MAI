from app.integrations.base import BaseIntegrationClient
from app.config import settings

class LinkedInAdsClient(BaseIntegrationClient):
    def __init__(self):
        super().__init__("https://api.linkedin.com/v2")
        self.headers = {"Authorization": f"Bearer {settings.LINKEDIN_ACCESS_TOKEN}"}
    
    async def check_connection(self) -> bool:
        return bool(settings.LINKEDIN_ACCESS_TOKEN)

class TwitterAdsClient(BaseIntegrationClient):
    def __init__(self):
        super().__init__("https://ads-api.twitter.com/12")
        # Auth logic for OAuth1.0a would be here
    
    async def check_connection(self) -> bool:
        return bool(settings.X_ADS_ACCESS_TOKEN)

class PinterestAdsClient(BaseIntegrationClient):
    def __init__(self):
        super().__init__("https://api.pinterest.com/v5")
        self.headers = {"Authorization": f"Bearer {settings.PINTEREST_ACCESS_TOKEN}"}

    async def check_connection(self) -> bool:
        return bool(settings.PINTEREST_ACCESS_TOKEN)
