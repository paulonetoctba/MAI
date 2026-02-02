from app.integrations.base import BaseIntegrationClient
from app.config import settings

class CommercetoolsClient(BaseIntegrationClient):
    def __init__(self):
        project_key = settings.COMMERCETOOLS_PROJECT_KEY
        super().__init__(f"https://api.us-central1.gcp.commercetools.com/{project_key}")
        
    async def check_connection(self) -> bool:
        return bool(settings.COMMERCETOOLS_CLIENT_ID)

class ElasticPathClient(BaseIntegrationClient):
    def __init__(self):
        super().__init__("https://api.elasticpath.com/v2")
        
    async def check_connection(self) -> bool:
        return bool(settings.ELASTIC_PATH_CLIENT_ID)

class VTEXIOClient(BaseIntegrationClient):
    """
    VTEX IO Client - Distinct from VTEX Legacy/Commerce if using IO workspaces.
    """
    def __init__(self):
        account = settings.VTEX_IO_ACCOUNT or settings.VTEX_ACCOUNT_NAME
        workspace = settings.VTEX_IO_WORKSPACE or "master"
        super().__init__(f"https://{workspace}--{account}.myvtex.com/_v/public/graphql")
        self.headers = {
            "X-VTEX-API-AppKey": settings.VTEX_IO_APP_KEY or settings.VTEX_APP_KEY,
            "X-VTEX-API-AppToken": settings.VTEX_IO_APP_TOKEN or settings.VTEX_APP_TOKEN
        }
        
    async def check_connection(self) -> bool:
        return bool(self.headers.get("X-VTEX-API-AppKey"))

class FabricClient(BaseIntegrationClient):
    def __init__(self):
        super().__init__("https://api.fabric.inc")
        self.headers = {"x-api-key": settings.FABRIC_API_KEY}
        
    async def check_connection(self) -> bool:
        return bool(settings.FABRIC_API_KEY)

class CommerceLayerClient(BaseIntegrationClient):
    def __init__(self):
        super().__init__("https://api.commercelayer.io")
        
    async def check_connection(self) -> bool:
        return bool(settings.COMMERCE_LAYER_CLIENT_ID)

class ScalefastClient(BaseIntegrationClient):
    def __init__(self):
        super().__init__("https://api.scalefast.com")
        
    async def check_connection(self) -> bool:
        return bool(settings.SCALEFAST_API_KEY)
