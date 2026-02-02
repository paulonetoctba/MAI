import asyncio
import os
import sys

print("Adding backend to path...")
# Add backend to path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("Importing session...")
from app.db.session import async_session, engine
print("Importing models...")
from app.models.integrations import Integration
print("Importing select...")
from sqlalchemy import select

INTEGRATIONS = [
    # ADS
    {
        "key": "google_ads",
        "name": "Google Ads",
        "category": "ads",
        "description": "Visualize e otimize suas campanhas de pesquisa e display.",
        "config_schema": {
            "developer_token": "string",
            "client_id": "string",
            "client_secret": "string",
            "refresh_token": "string"
        }
    },
    {
        "key": "meta_ads",
        "name": "Meta Ads",
        "category": "ads",
        "description": "Gestão estratégica de Facebook e Instagram Ads.",
        "config_schema": {
            "access_token": "password",
            "ad_account_id": "string"
        }
    },
    {
        "key": "tiktok_ads",
        "name": "TikTok Ads",
        "category": "ads",
        "description": "Alcance o público jovem com inteligência no TikTok.",
        "config_schema": {
            "access_token": "password",
            "advertiser_id": "string"
        }
    },
    # ECOMMERCE
    {
        "key": "vtex",
        "name": "VTEX",
        "category": "ecommerce",
        "description": "Sincronize vendas e estoque da sua loja VTEX.",
        "config_schema": {
            "account_name": "string",
            "environment": "string",
            "app_key": "string",
            "app_token": "password"
        }
    },
    {
        "key": "nuvemshop",
        "name": "Nuvemshop",
        "category": "ecommerce",
        "description": "Potencialize sua loja Nuvemshop com IA.",
        "config_schema": {
            "access_token": "password",
            "store_id": "string"
        }
    },
    {
        "key": "mercadolivre",
        "name": "Mercado Livre",
        "category": "ecommerce",
        "description": "Integração completa com o maior ecossistema da AL.",
        "config_schema": {
            "access_token": "password"
        }
    },
    {
        "key": "loja_integrada",
        "name": "Loja Integrada",
        "category": "ecommerce",
        "description": "Conecte sua Loja Integrada ao MAI.",
        "config_schema": {
            "api_key": "string",
            "app_key": "string"
        }
    },
    # TOOLS
    {
        "key": "semrush",
        "name": "SEMrush",
        "category": "tools",
        "description": "Análise de SEO e tráfego orgânico competitivo.",
        "config_schema": {
            "api_key": "password"
        }
    }
]

async def seed():
    print("🌱 Seeding integrations...")
    async with async_session() as session:
        for data in INTEGRATIONS:
            # Check if exists
            result = await session.execute(select(Integration).where(Integration.key == data["key"]))
            existing = result.scalar_one_or_none()
            
            if existing:
                print(f"  - {data['name']} already exists, updating...")
                existing.name = data["name"]
                existing.category = data["category"]
                existing.description = data["description"]
                existing.config_schema = data["config_schema"]
            else:
                print(f"  - Adding {data['name']}...")
                new_int = Integration(**data)
                session.add(new_int)
        
        await session.commit()
    print("✅ Done!")

if __name__ == "__main__":
    asyncio.run(seed())
