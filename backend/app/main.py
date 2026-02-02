from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from contextlib import asynccontextmanager
from loguru import logger
import sys

from app.config import settings
from app.api.v1 import auth, decisions, users, campaigns, knowledge, integrations

# Configure logging
logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="DEBUG" if settings.DEBUG else "INFO",
)

# Rate limiter
limiter = Limiter(key_func=get_remote_address)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle manager"""
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    yield
    logger.info("Shutting down MAI API")


# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="""
    MAI - Marketing Artificial Intelligence API
    
    Motor Estratégico de Decisão baseado em RAG proprietário,
    scoring determinístico e validação cruzada.
    
    ## Funcionalidades
    
    * **Decisões Estratégicas** - Avalia decisões de marketing com impacto real
    * **MAI Decision Score™** - Scoring determinístico (Impacto × Urgência ÷ Risco)
    * **Validação Cruzada** - Segunda opinião estratégica
    * **RAG Multi-Namespace** - Conhecimento proprietário segmentado
    * **Integrações** - Ads (Google, Meta, TikTok), SEO (SEMrush), Ecommerce (VTEX, ML, etc.)
    """,
    version=settings.APP_VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Add rate limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "version": settings.APP_VERSION}


# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API info"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "description": "Decision Intelligence para Marketing",
        "docs": "/docs",
    }


# Include API routers
app.include_router(
    auth.router,
    prefix=f"{settings.API_V1_PREFIX}/auth",
    tags=["Authentication"],
)

app.include_router(
    decisions.router,
    prefix=f"{settings.API_V1_PREFIX}/decisions",
    tags=["Decisions"],
)

app.include_router(
    users.router,
    prefix=f"{settings.API_V1_PREFIX}/users",
    tags=["Users"],
)

app.include_router(
    campaigns.router,
    prefix=f"{settings.API_V1_PREFIX}/campaigns",
    tags=["Campaigns"],
)

app.include_router(
    knowledge.router,
    prefix=f"{settings.API_V1_PREFIX}/knowledge",
    tags=["Knowledge"],
)

app.include_router(
    integrations.router,
    prefix=f"{settings.API_V1_PREFIX}/integrations",
    tags=["Integrations"],
)


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )
