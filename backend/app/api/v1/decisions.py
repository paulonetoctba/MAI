from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.db.session import get_db
from app.api.deps import get_current_verified_user
from app.models.user import User, Decision, AuditLog
from app.schemas.decision import (
    DecisionRequest,
    DecisionResponse,
    ScoreRequest,
    ScoreResponse,
    ValidationRequest,
    ValidationResponse,
    DecisionHistoryItem,
)
from app.engine.orchestrator import DecisionOrchestrator

router = APIRouter()


@router.post("/evaluate", response_model=DecisionResponse)
async def evaluate_decision(
    request: DecisionRequest,
    req: Request,
    current_user: User = Depends(get_current_verified_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Evaluate a strategic decision using the MAI engine.
    
    Executes the complete flow:
    1. RAG retrieval
    2. Diagnosis
    3. MAI Decision Score
    4. Cross validation
    5. Final verdict
    """
    
    # Initialize orchestrator
    orchestrator = DecisionOrchestrator()
    
    # Process decision
    result = await orchestrator.evaluate(
        question=request.question,
        context=request.context.model_dump(),
        user_id=current_user.id,
        tenant_id=current_user.tenant_id,
    )
    
    # Store decision in database
    decision = Decision(
        user_id=current_user.id,
        tenant_id=current_user.tenant_id,
        question=request.question,
        context=request.context.model_dump(),
        diagnosis=result.diagnosis,
        key_metrics=result.key_metrics,
        hidden_risks=result.hidden_risks,
        strategic_principle=result.strategic_principle,
        impact_score=result.decision_score.impact,
        risk_score=result.decision_score.risk,
        urgency_score=result.decision_score.urgency,
        mai_score=result.decision_score.score,
        mai_decision=result.mai_decision.value,
        validation_verdict=result.validation_verdict.value,
        next_step=result.next_step,
    )
    db.add(decision)
    
    # Audit log
    audit = AuditLog(
        user_id=current_user.id,
        tenant_id=current_user.tenant_id,
        action="decision.evaluated",
        resource_type="decision",
        resource_id=decision.id,
        ip_address=req.client.host if req.client else None,
        details={"question": request.question[:100], "score": result.decision_score.score},
    )
    db.add(audit)
    
    await db.commit()
    
    return result


@router.post("/score", response_model=ScoreResponse)
async def calculate_score(
    request: ScoreRequest,
    current_user: User = Depends(get_current_verified_user),
):
    """
    Calculate MAI Decision Score™
    
    Formula: Score = (Impact × Urgency) ÷ Risk
    
    Interpretation:
    - Score ≥ 6: EXECUTAR
    - Score 3-5.9: VALIDAR/AJUSTAR
    - Score < 3: NÃO EXECUTAR
    """
    
    return ScoreResponse.calculate(
        impact=request.impact,
        risk=request.risk,
        urgency=request.urgency,
    )


@router.post("/validate", response_model=ValidationResponse)
async def validate_decision(
    request: ValidationRequest,
    current_user: User = Depends(get_current_verified_user),
):
    """
    Cross-validate a decision (second opinion)
    
    Tests the robustness of the initial decision by:
    - Questioning assumptions
    - Analyzing negative scenarios
    - Checking ignored metrics
    - Verifying market principles
    """
    
    orchestrator = DecisionOrchestrator()
    
    result = await orchestrator.cross_validate(
        decision=request.decision,
        diagnosis=request.diagnosis,
        score=request.score,
        context=request.context.model_dump(),
    )
    
    return result


@router.get("/history", response_model=List[DecisionHistoryItem])
async def get_decision_history(
    limit: int = 20,
    offset: int = 0,
    current_user: User = Depends(get_current_verified_user),
    db: AsyncSession = Depends(get_db),
):
    """Get user's decision history"""
    
    result = await db.execute(
        select(Decision)
        .where(Decision.user_id == current_user.id)
        .order_by(Decision.created_at.desc())
        .limit(limit)
        .offset(offset)
    )
    decisions = result.scalars().all()
    
    return [
        DecisionHistoryItem(
            id=d.id,
            question=d.question,
            mai_decision=d.mai_decision,
            score=d.mai_score,
            created_at=d.created_at,
        )
        for d in decisions
    ]


@router.get("/{decision_id}", response_model=DecisionResponse)
async def get_decision(
    decision_id: str,
    current_user: User = Depends(get_current_verified_user),
    db: AsyncSession = Depends(get_db),
):
    """Get a specific decision by ID"""
    
    result = await db.execute(
        select(Decision).where(
            Decision.id == decision_id,
            Decision.user_id == current_user.id,
        )
    )
    decision = result.scalar_one_or_none()
    
    if not decision:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Decision not found",
        )
    
    return DecisionResponse(
        diagnosis=decision.diagnosis,
        key_metrics=decision.key_metrics or [],
        hidden_risks=decision.hidden_risks or [],
        strategic_principle=decision.strategic_principle,
        decision_score=ScoreResponse(
            impact=decision.impact_score,
            risk=decision.risk_score,
            urgency=decision.urgency_score,
            score=decision.mai_score,
            interpretation=decision.mai_decision,
        ),
        mai_decision=decision.mai_decision,
        next_step=decision.next_step,
        validation_verdict=decision.validation_verdict,
    )
