from app.integrations.base import BaseIntegrationClient
from app.config import settings

class WhatsAppBusinessClient(BaseIntegrationClient):
    def __init__(self):
        super().__init__("https://graph.facebook.com/v18.0")
        
    async def check_connection(self) -> bool:
        return bool(settings.WHATSAPP_BUSINESS_TOKEN)

class TwilioClient(BaseIntegrationClient):
    def __init__(self):
        sid = settings.TWILIO_ACCOUNT_SID
        super().__init__(f"https://api.twilio.com/2010-04-01/Accounts/{sid}")
        
    async def check_connection(self) -> bool:
        return bool(settings.TWILIO_ACCOUNT_SID)

class SendGridClient(BaseIntegrationClient):
    def __init__(self):
        super().__init__("https://api.sendgrid.com/v3")
        self.headers = {"Authorization": f"Bearer {settings.SENDGRID_API_KEY}"}
        
    async def check_connection(self) -> bool:
        return bool(settings.SENDGRID_API_KEY)
