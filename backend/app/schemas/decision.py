from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum
from datetime import datetime


class CompanyStage(str, Enum):
    TRACTION = "traction"
    SCALE = "scale"
    ENTERPRISE = "enterprise"


class DecisionType(str, Enum):
    GROWTH = "growth"
    BUDGET = "budget"
    PRODUCT = "product"
    PRICING = "pricing"
    MARKET = "market"


class MAIDecision(str, Enum):
    EXECUTAR = "EXECUTAR"
    AJUSTAR = "AJUSTAR"
    PAUSAR = "PAUSAR"
    BLOQUEAR = "BLOQUEAR"


class ValidationVerdict(str, Enum):
    CONFIRMAR = "CONFIRMAR"
    AJUSTAR = "AJUSTAR"
    BLOQUEAR = "BLOQUEAR"


# --- Request Schemas ---

class DecisionContext(BaseModel):
    """Context for decision evaluation"""
    company_stage: CompanyStage
    decision_type: DecisionType
    revenue_monthly: Optional[float] = None
    churn_rate: Optional[float] = None
    cac: Optional[float] = None
    ltv: Optional[float] = None
    gross_margin: Optional[float] = None
    burn_rate: Optional[float] = None
    additional_data: Optional[dict] = None


class DecisionRequest(BaseModel):
    """Request for decision evaluation"""
    question: str = Field(
        ...,
        min_length=10,
        description="The strategic question or decision to evaluate",
        example="Devemos escalar investimento em tráfego pago?"
    )
    context: DecisionContext


class ScoreRequest(BaseModel):
    """Request for MAI Decision Score calculation"""
    impact: int = Field(..., ge=1, le=5, description="Impact score (1-5)")
    risk: int = Field(..., ge=1, le=5, description="Risk score (1-5)")
    urgency: int = Field(..., ge=1, le=5, description="Urgency score (1-5)")


class ValidationRequest(BaseModel):
    """Request for cross-validation"""
    decision: str
    diagnosis: str
    score: "ScoreResponse"
    context: DecisionContext


# --- Response Schemas ---

class ScoreResponse(BaseModel):
    """MAI Decision Score response"""
    impact: int
    risk: int
    urgency: int
    score: float
    interpretation: str

    @staticmethod
    def calculate(impact: int, risk: int, urgency: int) -> "ScoreResponse":
        """Calculate MAI Decision Score"""
        score = (impact * urgency) / risk if risk > 0 else 0

        if score >= 6:
            interpretation = "EXECUTAR"
        elif score >= 3:
            interpretation = "VALIDAR"
        else:
            interpretation = "NÃO EXECUTAR"

        return ScoreResponse(
            impact=impact,
            risk=risk,
            urgency=urgency,
            score=round(score, 2),
            interpretation=interpretation,
        )


class DecisionResponse(BaseModel):
    """Complete decision evaluation response"""
    diagnosis: str
    key_metrics: List[str]
    hidden_risks: List[str]
    strategic_principle: str
    decision_score: ScoreResponse
    mai_decision: MAIDecision
    next_step: str
    validation_verdict: ValidationVerdict


class ValidationResponse(BaseModel):
    """Cross-validation response"""
    validation: ValidationVerdict
    additional_risks: List[str]
    final_verdict: str
    adjustments: Optional[List[str]] = None


class DecisionHistoryItem(BaseModel):
    """Historical decision item"""
    id: str
    question: str
    mai_decision: MAIDecision
    score: float
    created_at: datetime

    class Config:
        from_attributes = True


# Resolve forward reference
ValidationRequest.model_rebuild()
