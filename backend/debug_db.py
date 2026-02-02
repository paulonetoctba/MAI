import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import pool
from app.config import settings

async def test_engine():
    print(f"Testing URL: {settings.DATABASE_URL}")
    try:
        # Testing with poolclass=pool.NullPool
        engine = create_async_engine(settings.DATABASE_URL, echo=True, poolclass=pool.NullPool)
        async with engine.connect() as conn:
            print("✅ Connection Successful!")
        await engine.dispose()
    except Exception as e:
        print(f"❌ Connection Failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_engine())
