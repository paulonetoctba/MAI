"""
MAI Decision Scoring Engine

Implements the MAI Decision Score™ formula:
Score = (Impact × Urgency) ÷ Risk

Interpretation:
- Score ≥ 6: EXECUTAR
- Score 3-5.9: VALIDAR/AJUSTAR
- Score < 3: NÃO EXECUTAR

Each dimension is scored 1-5.
"""

from typing import Dict, Any, List
from loguru import logger

from app.schemas.decision import ScoreResponse


class ScoringEngine:
    """
    MAI Decision Score™ Calculator
    
    Evaluates strategic decisions using deterministic scoring
    based on three dimensions:
    - Impact: Financial and strategic potential
    - Risk: Downside exposure and reversibility
    - Urgency: Time sensitivity and opportunity cost
    """
    
    async def calculate(
        self,
        question: str,
        context: Dict[str, Any],
        diagnosis: str,
        hidden_risks: List[str],
    ) -> ScoreResponse:
        """
        Calculate the MAI Decision Score.
        
        Args:
            question: The strategic question
            context: Business context (metrics, stage, etc.)
            diagnosis: Strategic diagnosis
            hidden_risks: Identified risks
            
        Returns:
            ScoreResponse with score and interpretation
        """
        
        logger.info("Calculating MAI Decision Score...")
        
        # Calculate each dimension
        impact = self._calculate_impact(question, context)
        risk = self._calculate_risk(context, hidden_risks)
        urgency = self._calculate_urgency(question, context)
        
        # Apply formula
        score = (impact * urgency) / risk if risk > 0 else 0
        
        # Get interpretation
        interpretation = self._interpret_score(score)
        
        logger.info(f"MAI Score: {score:.2f} ({interpretation}) - I:{impact} R:{risk} U:{urgency}")
        
        return ScoreResponse(
            impact=impact,
            risk=risk,
            urgency=urgency,
            score=round(score, 2),
            interpretation=interpretation,
        )
    
    def _calculate_impact(
        self,
        question: str,
        context: Dict[str, Any],
    ) -> int:
        """
        Calculate Impact score (1-5)
        
        Criteria:
        - 5: Structural impact (revenue, margin, valuation)
        - 4: High and measurable impact
        - 3: Moderate impact
        - 2: Low impact
        - 1: Vanity metric / marginal effect
        """
        
        score = 3  # Base score
        
        # Check for high-impact keywords
        high_impact_words = ["receita", "margem", "ltv", "cac", "churn", "valuation"]
        low_impact_words = ["likes", "impressões", "followers", "awareness"]
        
        question_lower = question.lower()
        
        for word in high_impact_words:
            if word in question_lower:
                score += 1
                break
        
        for word in low_impact_words:
            if word in question_lower:
                score -= 1
                break
        
        # Context-based adjustments
        revenue = context.get("revenue_monthly", 0)
        if revenue > 500000:
            score += 1  # Higher stakes
        
        # Check decision type
        decision_type = context.get("decision_type", "")
        if decision_type in ["growth", "pricing"]:
            score += 1  # Strategic decisions
        
        return max(1, min(5, score))
    
    def _calculate_risk(
        self,
        context: Dict[str, Any],
        hidden_risks: List[str],
    ) -> int:
        """
        Calculate Risk score (1-5)
        
        Criteria:
        - 5: High risk / negative asymmetry
        - 4: Significant risk
        - 3: Manageable risk
        - 2: Low risk
        - 1: Almost no risk
        """
        
        score = 2  # Base score (some risk assumed)
        
        # Number of hidden risks
        if len(hidden_risks) >= 3:
            score += 2
        elif len(hidden_risks) >= 1:
            score += 1
        
        # Unit economics health
        ltv = context.get("ltv", 0)
        cac = context.get("cac", 0)
        churn = context.get("churn_rate", 0)
        
        if cac > 0 and ltv > 0:
            ltv_cac = ltv / cac
            if ltv_cac < 2:
                score += 2  # High risk
            elif ltv_cac < 3:
                score += 1  # Elevated risk
        
        if churn > 0.1:
            score += 1  # High churn = higher risk
        
        # Company stage
        stage = context.get("company_stage", "traction")
        if stage == "traction":
            score += 1  # Early stage = higher risk
        
        return max(1, min(5, score))
    
    def _calculate_urgency(
        self,
        question: str,
        context: Dict[str, Any],
    ) -> int:
        """
        Calculate Urgency score (1-5)
        
        Criteria:
        - 5: Critical window (delay destroys value)
        - 4: Time sensitive
        - 3: Can wait for validation
        - 2: Not urgent
        - 1: Can be delayed without impact
        """
        
        score = 3  # Base score
        
        # Check for urgency keywords
        urgent_words = ["agora", "urgente", "imediato", "janela", "oportunidade"]
        non_urgent_words = ["futuro", "planejar", "avaliar", "considerar"]
        
        question_lower = question.lower()
        
        for word in urgent_words:
            if word in question_lower:
                score += 1
                break
        
        for word in non_urgent_words:
            if word in question_lower:
                score -= 1
                break
        
        # Stage-based adjustments
        stage = context.get("company_stage", "traction")
        if stage == "traction":
            score -= 1  # In traction, validation > speed
        elif stage == "scale":
            score += 1  # In scale, speed matters more
        
        return max(1, min(5, score))
    
    def _interpret_score(self, score: float) -> str:
        """
        Interpret the final score.
        
        Returns:
            Interpretation string
        """
        
        if score >= 6:
            return "EXECUTAR"
        elif score >= 3:
            return "VALIDAR"
        else:
            return "NÃO EXECUTAR"
