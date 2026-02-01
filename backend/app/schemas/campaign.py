from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum
from datetime import datetime


class AdPlatform(str, Enum):
    GOOGLE = "google"
    META = "meta"
    LINKEDIN = "linkedin"


class CampaignStatus(str, Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    ERROR = "error"


# --- Request Schemas ---

class CampaignSyncRequest(BaseModel):
    """Request to sync campaign data from ad platform"""
    platform: AdPlatform
    start_date: str = Field(..., description="YYYY-MM-DD format")
    end_date: str = Field(..., description="YYYY-MM-DD format")


class CampaignFilterRequest(BaseModel):
    """Filter criteria for campaign queries"""
    platform: Optional[AdPlatform] = None
    status: Optional[CampaignStatus] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None


# --- Response Schemas ---

class CampaignMetrics(BaseModel):
    """Campaign performance metrics"""
    impressions: int = 0
    clicks: int = 0
    conversions: int = 0
    spend: float = 0.0
    revenue: float = 0.0
    ctr: float = 0.0
    cpc: float = 0.0
    cpa: float = 0.0
    roas: float = 0.0

    @staticmethod
    def calculate_derived(
        impressions: int,
        clicks: int,
        conversions: int,
        spend: float,
        revenue: float,
    ) -> "CampaignMetrics":
        """Calculate derived metrics"""
        ctr = (clicks / impressions * 100) if impressions > 0 else 0
        cpc = (spend / clicks) if clicks > 0 else 0
        cpa = (spend / conversions) if conversions > 0 else 0
        roas = (revenue / spend) if spend > 0 else 0

        return CampaignMetrics(
            impressions=impressions,
            clicks=clicks,
            conversions=conversions,
            spend=spend,
            revenue=revenue,
            ctr=round(ctr, 2),
            cpc=round(cpc, 2),
            cpa=round(cpa, 2),
            roas=round(roas, 2),
        )


class CampaignResponse(BaseModel):
    """Campaign data response"""
    id: str
    name: str
    platform: AdPlatform
    status: CampaignStatus
    metrics: CampaignMetrics
    start_date: str
    end_date: Optional[str] = None
    synced_at: datetime

    class Config:
        from_attributes = True


class CampaignListResponse(BaseModel):
    """List of campaigns response"""
    campaigns: List[CampaignResponse]
    total: int
    page: int
    per_page: int


class CampaignAggregateResponse(BaseModel):
    """Aggregated campaign metrics"""
    total_spend: float
    total_revenue: float
    total_conversions: int
    average_cpa: float
    average_roas: float
    by_platform: dict


class AdAccountResponse(BaseModel):
    """Connected ad account info"""
    id: str
    platform: AdPlatform
    account_name: str
    is_connected: bool
    last_sync: Optional[datetime] = None

    class Config:
        from_attributes = True
