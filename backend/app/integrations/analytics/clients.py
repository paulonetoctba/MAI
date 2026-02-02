from app.integrations.base import BaseIntegrationClient
from app.config import settings

class GoogleAnalyticsClient(BaseIntegrationClient):
    def __init__(self):
        super().__init__("https://analyticsdata.googleapis.com/v1beta")
    
    async def check_connection(self) -> bool:
        return bool(settings.GOOGLE_ANALYTICS_PROPERTY_ID)

class SearchConsoleClient(BaseIntegrationClient):
    def __init__(self):
        super().__init__("https://searchconsole.googleapis.com/webmasters/v3")
    
    async def check_connection(self) -> bool:
        return bool(settings.GOOGLE_SEARCH_CONSOLE_SITE_URL)
