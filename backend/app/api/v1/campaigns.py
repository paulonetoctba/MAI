from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List

from app.db.session import get_db
from app.api.deps import get_current_verified_user
from app.models.user import User, Campaign
from app.schemas.campaign import (
    CampaignSyncRequest,
    CampaignFilterRequest,
    CampaignResponse,
    CampaignListResponse,
    CampaignAggregateResponse,
    CampaignMetrics,
    AdAccountResponse,
    AdPlatform,
)
from app.schemas.auth import MessageResponse
from app.integrations.ads.google_ads import GoogleAdsClient
from app.integrations.ads.meta_ads import MetaAdsClient

router = APIRouter()


@router.get("/", response_model=CampaignListResponse)
async def list_campaigns(
    platform: AdPlatform = None,
    page: int = 1,
    per_page: int = 20,
    current_user: User = Depends(get_current_verified_user),
    db: AsyncSession = Depends(get_db),
):
    """List user's campaigns with optional platform filter"""
    
    offset = (page - 1) * per_page
    
    query = select(Campaign).where(Campaign.user_id == current_user.id)
    
    if platform:
        query = query.where(Campaign.platform == platform.value)
    
    query = query.order_by(Campaign.synced_at.desc()).limit(per_page).offset(offset)
    
    result = await db.execute(query)
    campaigns = result.scalars().all()
    
    # Count total
    count_query = select(Campaign).where(Campaign.user_id == current_user.id)
    if platform:
        count_query = count_query.where(Campaign.platform == platform.value)
    count_result = await db.execute(count_query)
    total = len(count_result.scalars().all())
    
    return CampaignListResponse(
        campaigns=[
            CampaignResponse(
                id=c.id,
                name=c.name,
                platform=c.platform,
                status=c.status,
                metrics=CampaignMetrics(
                    impressions=c.impressions,
                    clicks=c.clicks,
                    conversions=c.conversions,
                    spend=c.spend,
                    revenue=c.revenue,
                    ctr=c.ctr,
                    cpc=c.cpc,
                    cpa=c.cpa,
                    roas=c.roas,
                ),
                start_date=c.start_date,
                end_date=c.end_date,
                synced_at=c.synced_at,
            )
            for c in campaigns
        ],
        total=total,
        page=page,
        per_page=per_page,
    )


@router.get("/aggregate", response_model=CampaignAggregateResponse)
async def get_campaign_aggregates(
    current_user: User = Depends(get_current_verified_user),
    db: AsyncSession = Depends(get_db),
):
    """Get aggregated campaign metrics"""
    
    result = await db.execute(
        select(Campaign).where(Campaign.user_id == current_user.id)
    )
    campaigns = result.scalars().all()
    
    if not campaigns:
        return CampaignAggregateResponse(
            total_spend=0,
            total_revenue=0,
            total_conversions=0,
            average_cpa=0,
            average_roas=0,
            by_platform={},
        )
    
    total_spend = sum(c.spend for c in campaigns)
    total_revenue = sum(c.revenue for c in campaigns)
    total_conversions = sum(c.conversions for c in campaigns)
    
    # By platform
    by_platform = {}
    for c in campaigns:
        if c.platform not in by_platform:
            by_platform[c.platform] = {
                "spend": 0,
                "revenue": 0,
                "conversions": 0,
            }
        by_platform[c.platform]["spend"] += c.spend
        by_platform[c.platform]["revenue"] += c.revenue
        by_platform[c.platform]["conversions"] += c.conversions
    
    return CampaignAggregateResponse(
        total_spend=round(total_spend, 2),
        total_revenue=round(total_revenue, 2),
        total_conversions=total_conversions,
        average_cpa=round(total_spend / total_conversions, 2) if total_conversions > 0 else 0,
        average_roas=round(total_revenue / total_spend, 2) if total_spend > 0 else 0,
        by_platform=by_platform,
    )


@router.post("/sync/google", response_model=MessageResponse)
async def sync_google_ads(
    request: CampaignSyncRequest,
    current_user: User = Depends(get_current_verified_user),
    db: AsyncSession = Depends(get_db),
):
    """Sync campaigns from Google Ads"""
    
    try:
        client = GoogleAdsClient(user_id=current_user.id)
        campaigns = await client.fetch_campaigns(
            start_date=request.start_date,
            end_date=request.end_date,
        )
        
        # Store campaigns
        for campaign_data in campaigns:
            campaign = Campaign(
                user_id=current_user.id,
                tenant_id=current_user.tenant_id,
                external_id=campaign_data["id"],
                platform="google",
                name=campaign_data["name"],
                status=campaign_data["status"],
                impressions=campaign_data["impressions"],
                clicks=campaign_data["clicks"],
                conversions=campaign_data["conversions"],
                spend=campaign_data["spend"],
                revenue=campaign_data.get("revenue", 0),
                start_date=request.start_date,
                end_date=request.end_date,
            )
            # Calculate derived metrics
            metrics = CampaignMetrics.calculate_derived(
                impressions=campaign.impressions,
                clicks=campaign.clicks,
                conversions=campaign.conversions,
                spend=campaign.spend,
                revenue=campaign.revenue,
            )
            campaign.ctr = metrics.ctr
            campaign.cpc = metrics.cpc
            campaign.cpa = metrics.cpa
            campaign.roas = metrics.roas
            
            db.add(campaign)
        
        await db.commit()
        
        return MessageResponse(
            message=f"Successfully synced {len(campaigns)} campaigns from Google Ads"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to sync Google Ads: {str(e)}",
        )


@router.post("/sync/meta", response_model=MessageResponse)
async def sync_meta_ads(
    request: CampaignSyncRequest,
    current_user: User = Depends(get_current_verified_user),
    db: AsyncSession = Depends(get_db),
):
    """Sync campaigns from Meta Ads (Facebook/Instagram)"""
    
    try:
        client = MetaAdsClient(user_id=current_user.id)
        campaigns = await client.fetch_campaigns(
            start_date=request.start_date,
            end_date=request.end_date,
        )
        
        # Store campaigns
        for campaign_data in campaigns:
            campaign = Campaign(
                user_id=current_user.id,
                tenant_id=current_user.tenant_id,
                external_id=campaign_data["id"],
                platform="meta",
                name=campaign_data["name"],
                status=campaign_data["status"],
                impressions=campaign_data["impressions"],
                clicks=campaign_data["clicks"],
                conversions=campaign_data["conversions"],
                spend=campaign_data["spend"],
                revenue=campaign_data.get("revenue", 0),
                start_date=request.start_date,
                end_date=request.end_date,
            )
            # Calculate derived metrics
            metrics = CampaignMetrics.calculate_derived(
                impressions=campaign.impressions,
                clicks=campaign.clicks,
                conversions=campaign.conversions,
                spend=campaign.spend,
                revenue=campaign.revenue,
            )
            campaign.ctr = metrics.ctr
            campaign.cpc = metrics.cpc
            campaign.cpa = metrics.cpa
            campaign.roas = metrics.roas
            
            db.add(campaign)
        
        await db.commit()
        
        return MessageResponse(
            message=f"Successfully synced {len(campaigns)} campaigns from Meta Ads"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to sync Meta Ads: {str(e)}",
        )


@router.get("/accounts", response_model=List[AdAccountResponse])
async def list_ad_accounts(
    current_user: User = Depends(get_current_verified_user),
):
    """List connected ad accounts"""
    
    # TODO: Implement actual account storage
    return [
        AdAccountResponse(
            id="google_demo",
            platform=AdPlatform.GOOGLE,
            account_name="Demo Google Ads Account",
            is_connected=False,
        ),
        AdAccountResponse(
            id="meta_demo",
            platform=AdPlatform.META,
            account_name="Demo Meta Ads Account",
            is_connected=False,
        ),
        AdAccountResponse(
            id="tiktok_demo",
            platform=AdPlatform.TIKTOK,
            account_name="Demo TikTok Ads Account",
            is_connected=False,
        ),
    ]


@router.post("/sync/tiktok", response_model=MessageResponse)
async def sync_tiktok_ads(
    request: CampaignSyncRequest,
    current_user: User = Depends(get_current_verified_user),
    db: AsyncSession = Depends(get_db),
):
    """Sync campaigns from TikTok Ads"""
    
    try:
        from app.integrations.ads.tiktok_ads import TikTokAdsClient
        
        client = TikTokAdsClient(user_id=current_user.id)
        campaigns = await client.fetch_campaigns(
            start_date=request.start_date,
            end_date=request.end_date,
        )
        
        # Store campaigns
        for campaign_data in campaigns:
            campaign = Campaign(
                user_id=current_user.id,
                tenant_id=current_user.tenant_id,
                external_id=campaign_data["id"],
                platform="tiktok",
                name=campaign_data["name"],
                status=campaign_data["status"],
                impressions=campaign_data["impressions"],
                clicks=campaign_data["clicks"],
                conversions=campaign_data["conversions"],
                spend=campaign_data["spend"],
                revenue=campaign_data.get("revenue", 0),
                start_date=request.start_date,
                end_date=request.end_date,
            )
            # Calculate derived metrics
            metrics = CampaignMetrics.calculate_derived(
                impressions=campaign.impressions,
                clicks=campaign.clicks,
                conversions=campaign.conversions,
                spend=campaign.spend,
                revenue=campaign.revenue,
            )
            campaign.ctr = metrics.ctr
            campaign.cpc = metrics.cpc
            campaign.cpa = metrics.cpa
            campaign.roas = metrics.roas
            
            db.add(campaign)
        
        await db.commit()
        
        return MessageResponse(
            message=f"Successfully synced {len(campaigns)} campaigns from TikTok Ads"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to sync TikTok Ads: {str(e)}",
        )

