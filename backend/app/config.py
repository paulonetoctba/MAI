from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application Settings - Environment Variables"""

    # Application
    APP_NAME: str = "MAI - Marketing Artificial Intelligence"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"

    # API
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "MAI API"

    # Security
    SECRET_KEY: str = "your-super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./app.db"
    DATABASE_POOL_SIZE: int = 20

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # OpenAI
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4-turbo-preview"

    # Vector Database (Qdrant)
    QDRANT_HOST: str = "localhost"
    QDRANT_PORT: int = 6333
    QDRANT_API_KEY: Optional[str] = None

    # Email (SMTP)
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM_EMAIL: str = "noreply@mai.ai"
    SMTP_FROM_NAME: str = "MAI"

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60

    # CORS
    CORS_ORIGINS: list = ["http://localhost:3000", "https://mai.ai"]

    # Google Ads
    GOOGLE_ADS_DEVELOPER_TOKEN: str = ""
    GOOGLE_ADS_CLIENT_ID: str = ""
    GOOGLE_ADS_CLIENT_SECRET: str = ""

    # Meta Ads
    META_APP_ID: str = ""
    META_APP_SECRET: str = ""
    
    # VTEX Integration
    VTEX_ACCOUNT_NAME: str = ""
    VTEX_ENVIRONMENT: str = "vtexcommercestable"
    VTEX_APP_KEY: str = ""
    VTEX_APP_TOKEN: str = ""

    # --- ANALYTICS & INSIGHTS ---
    GOOGLE_ANALYTICS_PROPERTY_ID: str = ""
    GOOGLE_SEARCH_CONSOLE_SITE_URL: str = ""
    
    # --- ADS PLATFORMS ---
    # Google & YouTube
    YOUTUBE_ADS_DEVELOPER_TOKEN: str = ""
    
    # LinkedIn
    LINKEDIN_CLIENT_ID: str = ""
    LINKEDIN_CLIENT_SECRET: str = ""
    LINKEDIN_ACCESS_TOKEN: str = ""
    
    # TikTok
    TIKTOK_APP_ID: str = ""
    TIKTOK_SECRET: str = ""
    TIKTOK_ACCESS_TOKEN: str = ""
    
    # X (Twitter)
    X_ADS_CONSUMER_KEY: str = ""
    X_ADS_CONSUMER_SECRET: str = ""
    X_ADS_ACCESS_TOKEN: str = ""
    X_ADS_TOKEN_SECRET: str = ""
    
    # Pinterest
    PINTEREST_APP_ID: str = ""
    PINTEREST_APP_SECRET: str = ""
    PINTEREST_ACCESS_TOKEN: str = ""
    
    # Reddit
    REDDIT_CLIENT_ID: str = ""
    REDDIT_CLIENT_SECRET: str = ""
    REDDIT_ACCESS_TOKEN: str = ""
    
    # Retail Media (Amazon, ML, Shopee, Magalu, Walmart, AliExpress)
    AMAZON_ADS_CLIENT_ID: str = ""
    AMAZON_ADS_CLIENT_SECRET: str = ""
    MERCADO_ADS_APP_ID: str = ""
    MERCADO_ADS_SECRET: str = ""
    SHOPEE_ADS_PARTNER_ID: str = ""
    SHOPEE_ADS_KEY: str = ""
    MAGALU_ADS_ID: str = ""
    MAGALU_ADS_TOKEN: str = ""
    WALMART_CLIENT_ID: str = ""
    WALMART_CLIENT_SECRET: str = ""
    ALIEXPRESS_APP_KEY: str = ""
    ALIEXPRESS_SECRET: str = ""
    
    # Programmatic (DV360, TTD, Amazon DSP, Criteo, Adform)
    DV360_CLIENT_ID: str = ""
    DV360_CLIENT_SECRET: str = ""
    THE_TRADE_DESK_LOGIN: str = ""
    THE_TRADE_DESK_PASSWORD: str = ""
    CRITEO_CLIENT_ID: str = ""
    CRITEO_CLIENT_SECRET: str = ""
    ADFORM_CLIENT_ID: str = ""
    ADFORM_CLIENT_SECRET: str = ""

    # --- CRM & MARKETING AUTOMATION ---
    SALESFORCE_MC_CLIENT_ID: str = ""
    SALESFORCE_MC_CLIENT_SECRET: str = ""
    HUBSPOT_ACCESS_TOKEN: str = ""
    RD_STATION_CLIENT_ID: str = ""
    RD_STATION_CLIENT_SECRET: str = ""
    MAILCHIMP_API_KEY: str = ""
    MAILCHIMP_SERVER_PREFIX: str = ""
    ACTIVECAMPAIGN_URL: str = ""
    ACTIVECAMPAIGN_KEY: str = ""
    KLAVIYO_PUBLIC_KEY: str = ""
    KLAVIYO_PRIVATE_KEY: str = ""
    BRAZE_API_KEY: str = ""
    BRAZE_REST_ENDPOINT: str = ""

    # --- COMMUNICATION ---
    WHATSAPP_BUSINESS_TOKEN: str = ""
    WHATSAPP_PHONE_NUMBER_ID: str = ""
    TWILIO_ACCOUNT_SID: str = ""
    TWILIO_AUTH_TOKEN: str = ""
    SENDGRID_API_KEY: str = ""
    FIREBASE_CREDENTIALS_PATH: str = ""

    # --- ECOMMERCE PLATFORMS ---
    # VTEX (Already added, keeping for reference)
    # VTEX_ACCOUNT_NAME: str = "" ...
    
    SHOPIFY_SHOP_URL: str = ""
    SHOPIFY_ACCESS_TOKEN: str = ""
    
    BIGCOMMERCE_STORE_HASH: str = ""
    BIGCOMMERCE_ACCESS_TOKEN: str = ""
    
    SALESFORCE_CC_CLIENT_ID: str = ""
    
    SAP_COMMERCE_URL: str = ""
    
    ORACLE_COMMERCE_URL: str = ""
    
    
    WIX_API_KEY: str = ""
    
    SQUARESPACE_API_KEY: str = ""
    
    # --- LATAM ECOMMERCE ---
    NUVEMSHOP_CLIENT_ID: str = ""
    NUVEMSHOP_CLIENT_SECRET: str = ""
    NUVEMSHOP_ACCESS_TOKEN: str = ""
    
    LOJA_INTEGRADA_API_KEY: str = ""
    LOJA_INTEGRADA_APP_KEY: str = ""
    
    TRAY_CONSUMER_KEY: str = ""
    TRAY_CONSUMER_SECRET: str = ""
    TRAY_CODE: str = ""
    
    YAMPI_USER_TOKEN: str = ""
    YAMPI_USER_SECRET: str = ""
    
    WAKE_COMMERCE_TOKEN: str = ""
    
    VNDA_ACCESS_TOKEN: str = ""
    VNDA_HOST: str = ""
    
    DOOCA_TOKEN: str = ""
    
    JET_COMMERCE_CLIENT_ID: str = ""
    JET_COMMERCE_CLIENT_SECRET: str = ""
    
    # --- HEADLESS / ENTERPRISE COMMERCE ---
    COMMERCETOOLS_CLIENT_ID: str = ""
    COMMERCETOOLS_CLIENT_SECRET: str = ""
    COMMERCETOOLS_PROJECT_KEY: str = ""
    
    ELASTIC_PATH_CLIENT_ID: str = ""
    ELASTIC_PATH_CLIENT_SECRET: str = ""
    
    VTEX_IO_ACCOUNT: str = "" 
    VTEX_IO_WORKSPACE: str = ""
    VTEX_IO_APP_KEY: str = ""
    VTEX_IO_APP_TOKEN: str = ""
    
    FABRIC_API_KEY: str = ""
    FABRIC_ACCOUNT_ID: str = ""
    
    COMMERCE_LAYER_CLIENT_ID: str = ""
    COMMERCE_LAYER_CLIENT_SECRET: str = ""
    
    SCALEFAST_API_KEY: str = ""
    
    # --- TOOLS ---
    SEMRUSH_API_KEY: str = ""

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
