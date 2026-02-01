# MAI Schemas Package
from app.schemas.auth import (
    UserRegisterRequest,
    UserLoginRequest,
    TokenResponse,
    UserResponse,
)
from app.schemas.decision import (
    DecisionRequest,
    DecisionResponse,
    ScoreRequest,
    ScoreResponse,
)
from app.schemas.campaign import (
    CampaignResponse,
    CampaignMetrics,
)
from app.schemas.user import (
    UserProfileResponse,
    APIKeyResponse,
)
