from app.integrations.base import BaseIntegrationClient
from app.config import settings

class NuvemshopClient(BaseIntegrationClient):
    def __init__(self):
        super().__init__("https://api.nuvemshop.com.br/v1")
        self.headers = {"Authentication": f"bearer {settings.NUVEMSHOP_ACCESS_TOKEN}"}
        
    async def check_connection(self) -> bool:
        return bool(settings.NUVEMSHOP_ACCESS_TOKEN)

class LojaIntegradaClient(BaseIntegrationClient):
    def __init__(self):
        super().__init__("https://api.awsli.com.br/v1")
        self.headers = {
            "Authorization": f"chave_api {settings.LOJA_INTEGRADA_API_KEY} aplicacao {settings.LOJA_INTEGRADA_APP_KEY}"
        }
        
    async def check_connection(self) -> bool:
        return bool(settings.LOJA_INTEGRADA_API_KEY and settings.LOJA_INTEGRADA_APP_KEY)

class TrayClient(BaseIntegrationClient):
    def __init__(self):
        super().__init__("https://api.tray.com.br")
        # Tray usually requires a specific store URL + OAuth
        
    async def check_connection(self) -> bool:
        return bool(settings.TRAY_CONSUMER_KEY)

class YampiClient(BaseIntegrationClient):
    def __init__(self):
        super().__init__("https://api.yampi.io/v1")
        self.headers = {
            "User-Token": settings.YAMPI_USER_TOKEN,
            "User-Secret": settings.YAMPI_USER_SECRET
        }
        
    async def check_connection(self) -> bool:
        return bool(settings.YAMPI_USER_TOKEN)

class WakeCommerceClient(BaseIntegrationClient):
    def __init__(self):
        super().__init__("https://api.fbits.net") # Default endpoint, varies by usage
        self.headers = {"Authorization": f"Basic {settings.WAKE_COMMERCE_TOKEN}"}
        
    async def check_connection(self) -> bool:
        return bool(settings.WAKE_COMMERCE_TOKEN)

class VndaClient(BaseIntegrationClient):
    def __init__(self):
        host = settings.VNDA_HOST or "api.vnda.com.br"
        super().__init__(f"https://{host}/api/v2")
        self.headers = {"Authorization": f"Bearer {settings.VNDA_ACCESS_TOKEN}"}
        
    async def check_connection(self) -> bool:
        return bool(settings.VNDA_ACCESS_TOKEN)

class DoocaClient(BaseIntegrationClient):
    def __init__(self):
        super().__init__("https://api.dooca.store")
        self.headers = {"Authorization": f"Bearer {settings.DOOCA_TOKEN}"}
        
    async def check_connection(self) -> bool:
        return bool(settings.DOOCA_TOKEN)

class JetCommerceClient(BaseIntegrationClient):
    def __init__(self):
        super().__init__("https://api.jet.com.br")
        
    async def check_connection(self) -> bool:
        return bool(settings.JET_COMMERCE_CLIENT_ID)
