from app.integrations.base import BaseIntegrationClient
from app.config import settings

class SalesforceMCClient(BaseIntegrationClient):
    def __init__(self):
        super().__init__("https://api.marketingcloudapis.com")
        
    async def check_connection(self) -> bool:
        return bool(settings.SALESFORCE_MC_CLIENT_ID)

class HubSpotClient(BaseIntegrationClient):
    def __init__(self):
        super().__init__("https://api.hubapi.com")
        self.headers = {"Authorization": f"Bearer {settings.HUBSPOT_ACCESS_TOKEN}"}
        
    async def check_connection(self) -> bool:
        return bool(settings.HUBSPOT_ACCESS_TOKEN)

class RDStationClient(BaseIntegrationClient):
    def __init__(self):
        super().__init__("https://api.rd.services/platform")
        
    async def check_connection(self) -> bool:
        return bool(settings.RD_STATION_CLIENT_ID)

class MailchimpClient(BaseIntegrationClient):
    def __init__(self):
        dc = settings.MAILCHIMP_SERVER_PREFIX
        super().__init__(f"https://{dc}.api.mailchimp.com/3.0")
        
    async def check_connection(self) -> bool:
        return bool(settings.MAILCHIMP_API_KEY)
