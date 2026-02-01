"""
MAI Response Formatter

Formats decision engine output for presentation.
"""

from typing import Dict, Any


class ResponseFormatter:
    """
    Formats MAI responses for clear, executive presentation.
    """
    
    @staticmethod
    def format_decision_response(
        diagnosis: str,
        key_metrics: list,
        hidden_risks: list,
        strategic_principle: str,
        score: Dict[str, Any],
        mai_decision: str,
        next_step: str,
        validation_verdict: str,
    ) -> Dict[str, Any]:
        """Format complete decision response"""
        
        return {
            "diagnosis": diagnosis,
            "key_metrics": key_metrics,
            "hidden_risks": hidden_risks,
            "strategic_principle": strategic_principle,
            "decision_score": score,
            "mai_decision": mai_decision,
            "next_step": next_step,
            "validation_verdict": validation_verdict,
        }
    
    @staticmethod
    def format_score(
        impact: int,
        risk: int,
        urgency: int,
        score: float,
        interpretation: str,
    ) -> Dict[str, Any]:
        """Format score response"""
        
        return {
            "impact": impact,
            "risk": risk,
            "urgency": urgency,
            "score": score,
            "interpretation": interpretation,
            "formula": "Score = (Impacto × Urgência) ÷ Risco",
        }
    
    @staticmethod
    def format_markdown_report(
        diagnosis: str,
        key_metrics: list,
        hidden_risks: list,
        strategic_principle: str,
        mai_decision: str,
        next_step: str,
    ) -> str:
        """Format as markdown report"""
        
        return f"""
# MAI Strategic Decision Report

## Diagnóstico
{diagnosis}

## Métricas-Chave
{chr(10).join(f"- {m}" for m in key_metrics)}

## Riscos Ocultos
{chr(10).join(f"- {r}" for r in hidden_risks)}

## Princípio Estratégico
> {strategic_principle}

## Decisão MAI
**{mai_decision}**

## Próximo Passo
{next_step}
"""
