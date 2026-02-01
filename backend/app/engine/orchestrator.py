"""
MAI Decision Orchestrator

Central component that orchestrates the complete decision evaluation flow:
1. Input classification
2. RAG retrieval
3. Strategic diagnosis
4. MAI Decision Score
5. Initial decision
6. Cross validation
7. Final verdict
"""

from typing import Dict, Any, Optional
from loguru import logger

from app.engine.rag_engine import RAGEngine
from app.engine.scoring_engine import ScoringEngine
from app.engine.validation_engine import ValidationEngine
from app.engine.response_formatter import ResponseFormatter
from app.schemas.decision import (
    DecisionResponse,
    ScoreResponse,
    ValidationResponse,
    MAIDecision,
    ValidationVerdict,
    DecisionType,
)


class DecisionOrchestrator:
    """
    Orchestrates the complete MAI decision evaluation pipeline.
    
    Flow:
    ┌────────────────────────────────┐
    │     Strategic Question         │
    └───────────────┬────────────────┘
                    ↓
    ┌────────────────────────────────┐
    │   Decision Classification      │
    │ Growth | Budget | Product | ...|
    └───────────────┬────────────────┘
                    ↓
    ┌────────────────────────────────┐
    │      RAG Retrieval             │
    │  (Multi-namespace search)      │
    └───────────────┬────────────────┘
                    ↓
    ┌────────────────────────────────┐
    │   Strategic Diagnosis          │
    │  (LLM-powered analysis)        │
    └───────────────┬────────────────┘
                    ↓
    ┌────────────────────────────────┐
    │   MAI Decision Score™          │
    │ Impact × Urgency ÷ Risk        │
    └───────────────┬────────────────┘
                    ↓
    ┌────────────────────────────────┐
    │   Initial MAI Decision         │
    │ EXECUTAR | AJUSTAR | PAUSAR    │
    └───────────────┬────────────────┘
                    ↓
    ┌────────────────────────────────┐
    │   Cross Validation             │
    │  (Second strategic opinion)    │
    └───────────────┬────────────────┘
                    ↓
    ┌────────────────────────────────┐
    │   Final Verdict                │
    │ CONFIRMAR | AJUSTAR | BLOQUEAR │
    └────────────────────────────────┘
    """
    
    def __init__(self):
        self.rag_engine = RAGEngine()
        self.scoring_engine = ScoringEngine()
        self.validation_engine = ValidationEngine()
        self.formatter = ResponseFormatter()
    
    async def evaluate(
        self,
        question: str,
        context: Dict[str, Any],
        user_id: str,
        tenant_id: str,
    ) -> DecisionResponse:
        """
        Execute the complete decision evaluation pipeline.
        
        Args:
            question: The strategic question to evaluate
            context: Business context (metrics, stage, etc.)
            user_id: ID of the requesting user
            tenant_id: Tenant ID for data isolation
            
        Returns:
            Complete decision response with diagnosis, score, and recommendation
        """
        
        logger.info(f"Evaluating decision for user {user_id}: {question[:50]}...")
        
        # Step 1: Classify decision type
        decision_type = self._classify_decision(question, context)
        logger.debug(f"Decision classified as: {decision_type}")
        
        # Step 2: Retrieve relevant knowledge from RAG
        namespaces = self._get_relevant_namespaces(decision_type)
        rag_context = await self.rag_engine.retrieve_multi_namespace(
            query=question,
            namespaces=namespaces,
            context=context,
        )
        logger.debug(f"Retrieved context from {len(namespaces)} namespaces")
        
        # Step 3: Generate strategic diagnosis
        diagnosis = await self._generate_diagnosis(question, context, rag_context)
        
        # Step 4: Identify key metrics and hidden risks
        key_metrics = self._identify_key_metrics(context, decision_type)
        hidden_risks = await self._identify_hidden_risks(question, context, rag_context)
        
        # Step 5: Identify applicable strategic principle
        strategic_principle = self._get_strategic_principle(decision_type, context)
        
        # Step 6: Calculate MAI Decision Score
        score = await self.scoring_engine.calculate(
            question=question,
            context=context,
            diagnosis=diagnosis,
            hidden_risks=hidden_risks,
        )
        
        # Step 7: Generate initial decision
        mai_decision = self._generate_initial_decision(score)
        
        # Step 8: Cross validation
        validation = await self.cross_validate(
            decision=mai_decision.value,
            diagnosis=diagnosis,
            score=score,
            context=context,
        )
        
        # Step 9: Generate next step recommendation
        next_step = self._generate_next_step(mai_decision, validation, context)
        
        logger.info(f"Decision evaluation complete: {mai_decision.value} (Score: {score.score})")
        
        return DecisionResponse(
            diagnosis=diagnosis,
            key_metrics=key_metrics,
            hidden_risks=hidden_risks,
            strategic_principle=strategic_principle,
            decision_score=score,
            mai_decision=mai_decision,
            next_step=next_step,
            validation_verdict=ValidationVerdict(validation.validation.value),
        )
    
    async def cross_validate(
        self,
        decision: str,
        diagnosis: str,
        score: ScoreResponse,
        context: Dict[str, Any],
    ) -> ValidationResponse:
        """
        Execute cross-validation of decision (second opinion).
        """
        return await self.validation_engine.validate(
            decision=decision,
            diagnosis=diagnosis,
            score=score,
            context=context,
        )
    
    def _classify_decision(
        self,
        question: str,
        context: Dict[str, Any],
    ) -> DecisionType:
        """Classify the type of decision being evaluated"""
        
        # Use context if provided
        if "decision_type" in context:
            return DecisionType(context["decision_type"])
        
        # Simple keyword-based classification
        question_lower = question.lower()
        
        if any(word in question_lower for word in ["escalar", "crescer", "aquisição", "tráfego"]):
            return DecisionType.GROWTH
        elif any(word in question_lower for word in ["budget", "orçamento", "investir", "gastar"]):
            return DecisionType.BUDGET
        elif any(word in question_lower for word in ["produto", "feature", "lançar"]):
            return DecisionType.PRODUCT
        elif any(word in question_lower for word in ["preço", "pricing", "desconto"]):
            return DecisionType.PRICING
        elif any(word in question_lower for word in ["mercado", "segmento", "expansão"]):
            return DecisionType.MARKET
        
        return DecisionType.GROWTH
    
    def _get_relevant_namespaces(self, decision_type: DecisionType) -> list:
        """Get RAG namespaces relevant to the decision type"""
        
        namespace_mapping = {
            DecisionType.GROWTH: ["growth_capital", "unit_economics", "funnel_economics"],
            DecisionType.BUDGET: ["growth_capital", "performance_revenue"],
            DecisionType.PRODUCT: ["behavioral_demand", "market_sizing"],
            DecisionType.PRICING: ["behavioral_demand", "unit_economics"],
            DecisionType.MARKET: ["market_sizing", "growth_capital"],
        }
        
        return namespace_mapping.get(decision_type, ["growth_capital"])
    
    async def _generate_diagnosis(
        self,
        question: str,
        context: Dict[str, Any],
        rag_context: list,
    ) -> str:
        """Generate strategic diagnosis of the situation"""
        
        # In production, this would use LLM
        # For now, generate based on context
        stage = context.get("company_stage", "traction")
        ltv = context.get("ltv", 0)
        cac = context.get("cac", 0)
        churn = context.get("churn_rate", 0)
        
        ltv_cac_ratio = ltv / cac if cac > 0 else 0
        
        if ltv_cac_ratio < 3:
            return f"O LTV/CAC atual ({ltv_cac_ratio:.1f}x) está abaixo do mínimo saudável (3x). Escalar aquisição agora pode acelerar a queima de caixa sem garantia de retorno."
        elif churn > 0.1:
            return f"O churn atual ({churn*100:.1f}%) indica problemas de retenção. Crescimento neste cenário é potencialmente artificial."
        else:
            return f"Os unit economics indicam fundamentos saudáveis (LTV/CAC: {ltv_cac_ratio:.1f}x, Churn: {churn*100:.1f}%). A decisão deve considerar capital efficiency."
    
    def _identify_key_metrics(
        self,
        context: Dict[str, Any],
        decision_type: DecisionType,
    ) -> list:
        """Identify key metrics for the decision"""
        
        metrics_mapping = {
            DecisionType.GROWTH: ["CAC Payback", "LTV/CAC", "Burn Multiple", "Churn por coorte"],
            DecisionType.BUDGET: ["ROAS Incremental", "Contribution Margin", "ROI marginal"],
            DecisionType.PRODUCT: ["Activation Rate", "Retention", "NPS"],
            DecisionType.PRICING: ["Elasticidade de preço", "Ticket médio", "Churn por preço"],
            DecisionType.MARKET: ["TAM realista", "SAM", "SOM", "Penetração"],
        }
        
        return metrics_mapping.get(decision_type, ["CAC", "LTV", "Churn"])
    
    async def _identify_hidden_risks(
        self,
        question: str,
        context: Dict[str, Any],
        rag_context: list,
    ) -> list:
        """Identify hidden risks in the decision"""
        
        risks = []
        
        ltv = context.get("ltv", 0)
        cac = context.get("cac", 0)
        churn = context.get("churn_rate", 0)
        
        if cac > 0 and ltv / cac < 3:
            risks.append("Unit economics frágeis - risco de escala prematura")
        
        if churn > 0.08:
            risks.append("Churn elevado indica problema de produto, não de aquisição")
        
        if "escalar" in question.lower() or "dobrar" in question.lower():
            risks.append("Aumento de investimento pode elevar CAC (diminishing returns)")
        
        if context.get("company_stage") == "traction":
            risks.append("Fase de tração exige validação antes de escala")
        
        if not risks:
            risks.append("Sem riscos críticos identificados, mas validar premissas")
        
        return risks
    
    def _get_strategic_principle(
        self,
        decision_type: DecisionType,
        context: Dict[str, Any],
    ) -> str:
        """Get applicable strategic principle"""
        
        principles = {
            DecisionType.GROWTH: "Eficiência de capital: crescer apenas quando unit economics comprovados",
            DecisionType.BUDGET: "ROI marginal: cada real adicional deve gerar retorno mensurável",
            DecisionType.PRODUCT: "Validação antes de escala: retenção > aquisição",
            DecisionType.PRICING: "Willingness to pay: preço deve refletir valor percebido",
            DecisionType.MARKET: "Bottom-up sizing: TAM não é garantia de captura",
        }
        
        return principles.get(decision_type, "Decisões baseadas em dados, não intuição")
    
    def _generate_initial_decision(self, score: ScoreResponse) -> MAIDecision:
        """Generate initial decision based on score"""
        
        if score.score >= 6:
            return MAIDecision.EXECUTAR
        elif score.score >= 4:
            return MAIDecision.AJUSTAR
        elif score.score >= 2:
            return MAIDecision.PAUSAR
        else:
            return MAIDecision.BLOQUEAR
    
    def _generate_next_step(
        self,
        decision: MAIDecision,
        validation: ValidationResponse,
        context: Dict[str, Any],
    ) -> str:
        """Generate concrete next step recommendation"""
        
        if validation.validation == ValidationVerdict.BLOQUEAR:
            return "Não executar. Revisitar premissas fundamentais antes de qualquer ação."
        
        if decision == MAIDecision.EXECUTAR:
            return "Executar com monitoramento semanal de métricas-chave. Definir critérios de reversão."
        elif decision == MAIDecision.AJUSTAR:
            return "Ajustar escopo ou cronograma. Validar hipóteses com teste controlado antes de escala."
        elif decision == MAIDecision.PAUSAR:
            return "Pausar e priorizar correção de fundamentos (retenção, unit economics). Revisitar em 30 dias."
        else:
            return "Bloquear execução. Risco de destruição de valor supera potencial de ganho."
