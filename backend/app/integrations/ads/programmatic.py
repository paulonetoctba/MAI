from app.integrations.base import BaseIntegrationClient
from app.config import settings

class DV360Client(BaseIntegrationClient):
    def __init__(self):
        super().__init__("https://displayvideo.googleapis.com/v2")
    
    async def check_connection(self) -> bool:
        return bool(settings.DV360_CLIENT_ID)

class TradeDeskClient(BaseIntegrationClient):
    def __init__(self):
        super().__init__("https://api.thetradedesk.com/v3")
        
    async def check_connection(self) -> bool:
        return bool(settings.THE_TRADE_DESK_LOGIN)

class CriteoClient(BaseIntegrationClient):
    def __init__(self):
        super().__init__("https://api.criteo.com")

    async def check_connection(self) -> bool:
        return bool(settings.CRITEO_CLIENT_ID)
