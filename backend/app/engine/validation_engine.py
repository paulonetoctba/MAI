"""
MAI Cross Validation Engine

Second strategic opinion that tests the robustness of initial decisions.

The validation engine:
- Questions assumptions
- Analyzes negative scenarios
- Checks for ignored metrics
- Verifies market principles
- Issues final verdict: CONFIRMAR | AJUSTAR | BLOQUEAR
"""

from typing import Dict, Any
from loguru import logger

from app.schemas.decision import (
    ScoreResponse,
    ValidationResponse,
    ValidationVerdict,
)


class ValidationEngine:
    """
    Cross-validation engine for strategic decisions.
    
    Acts as a "devil's advocate" to stress-test decisions
    before they are finalized.
    """
    
    async def validate(
        self,
        decision: str,
        diagnosis: str,
        score: ScoreResponse,
        context: Dict[str, Any],
    ) -> ValidationResponse:
        """
        Validate a decision through critical analysis.
        
        Args:
            decision: Initial MAI decision
            diagnosis: Strategic diagnosis
            score: Decision score details
            context: Business context
            
        Returns:
            ValidationResponse with verdict and adjustments
        """
        
        logger.info(f"Cross-validating decision: {decision}")
        
        # Collect additional risks
        additional_risks = await self._find_additional_risks(
            decision=decision,
            diagnosis=diagnosis,
            score=score,
            context=context,
        )
        
        # Check assumptions
        assumption_issues = self._check_assumptions(context)
        
        # Check for metric blind spots
        blind_spots = self._check_blind_spots(context)
        
        # Generate verdict
        verdict = self._determine_verdict(
            decision=decision,
            score=score,
            additional_risks=additional_risks + assumption_issues + blind_spots,
            context=context,
        )
        
        # Generate adjustments if needed
        adjustments = None
        if verdict == ValidationVerdict.AJUSTAR:
            adjustments = self._generate_adjustments(context, additional_risks)
        
        # Final verdict text
        final_verdict = self._generate_final_verdict(
            decision=decision,
            verdict=verdict,
            additional_risks=additional_risks,
        )
        
        logger.info(f"Validation complete: {verdict.value}")
        
        return ValidationResponse(
            validation=verdict,
            additional_risks=additional_risks + assumption_issues + blind_spots,
            final_verdict=final_verdict,
            adjustments=adjustments,
        )
    
    async def _find_additional_risks(
        self,
        decision: str,
        diagnosis: str,
        score: ScoreResponse,
        context: Dict[str, Any],
    ) -> list:
        """Find risks not identified in initial analysis"""
        
        risks = []
        
        # High impact + high risk combination
        if score.impact >= 4 and score.risk >= 4:
            risks.append("Alto impacto com alto risco: garantir capacidade de reversão")
        
        # Low urgency being treated as urgent
        if score.urgency <= 2 and decision in ["EXECUTAR"]:
            risks.append("Decisão executar com baixa urgência: risco de precipitação")
        
        # Churn risk
        churn = context.get("churn_rate", 0)
        if churn > 0.05 and decision != "PAUSAR":
            risks.append("Churn elevado pode invalidar premissas de crescimento")
        
        # Margin risk
        gross_margin = context.get("gross_margin", 0)
        if gross_margin > 0 and gross_margin < 0.6:
            risks.append("Margem bruta abaixo de 60% limita capacidade de investir em aquisição")
        
        return risks
    
    def _check_assumptions(self, context: Dict[str, Any]) -> list:
        """Check critical assumptions"""
        
        issues = []
        
        # LTV assumption
        ltv = context.get("ltv", 0)
        cac = context.get("cac", 0)
        
        if ltv > 0 and cac > 0:
            if ltv / cac < 3:
                issues.append("Premissa de LTV/CAC > 3x não confirmada")
        
        # Stage assumption
        stage = context.get("company_stage", "")
        revenue = context.get("revenue_monthly", 0)
        
        if stage == "scale" and revenue < 100000:
            issues.append("Stage 'scale' declarado mas revenue indica 'traction'")
        
        return issues
    
    def _check_blind_spots(self, context: Dict[str, Any]) -> list:
        """Check for ignored metrics or blind spots"""
        
        blind_spots = []
        
        # Missing critical metrics
        if context.get("churn_rate") is None:
            blind_spots.append("Métrica de churn não fornecida - risco não quantificável")
        
        if context.get("cac") is None or context.get("ltv") is None:
            blind_spots.append("Unit economics incompletos - decisão sem fundamento")
        
        return blind_spots
    
    def _determine_verdict(
        self,
        decision: str,
        score: ScoreResponse,
        additional_risks: list,
        context: Dict[str, Any],
    ) -> ValidationVerdict:
        """Determine final validation verdict"""
        
        # BLOQUEAR if too many additional risks
        if len(additional_risks) >= 4:
            return ValidationVerdict.BLOQUEAR
        
        # BLOQUEAR if unit economics are broken
        ltv = context.get("ltv", 0)
        cac = context.get("cac", 1)
        if ltv > 0 and cac > 0 and ltv / cac < 2:
            return ValidationVerdict.BLOQUEAR
        
        # AJUSTAR if moderate concerns
        if len(additional_risks) >= 2:
            return ValidationVerdict.AJUSTAR
        
        # AJUSTAR if score is borderline
        if 3 <= score.score < 5:
            return ValidationVerdict.AJUSTAR
        
        # CONFIRMAR if solid decision
        return ValidationVerdict.CONFIRMAR
    
    def _generate_adjustments(
        self,
        context: Dict[str, Any],
        risks: list,
    ) -> list:
        """Generate recommended adjustments"""
        
        adjustments = []
        
        if any("churn" in r.lower() for r in risks):
            adjustments.append("Priorizar correção de retenção antes de escalar aquisição")
        
        if any("ltv" in r.lower() or "cac" in r.lower() for r in risks):
            adjustments.append("Validar unit economics com dados recentes antes de executar")
        
        if any("urgência" in r.lower() for r in risks):
            adjustments.append("Realizar teste controlado de 2 semanas antes de escala completa")
        
        if not adjustments:
            adjustments.append("Implementar com monitoramento reforçado e critérios de reversão claros")
        
        return adjustments
    
    def _generate_final_verdict(
        self,
        decision: str,
        verdict: ValidationVerdict,
        additional_risks: list,
    ) -> str:
        """Generate human-readable final verdict"""
        
        if verdict == ValidationVerdict.CONFIRMAR:
            return f"Decisão '{decision}' validada. Fundamentos sólidos, riscos mapeados."
        
        elif verdict == ValidationVerdict.AJUSTAR:
            return f"Decisão '{decision}' requer ajustes. {len(additional_risks)} riscos adicionais identificados."
        
        else:  # BLOQUEAR
            return f"Decisão '{decision}' BLOQUEADA. Riscos superam benefícios no cenário atual."
