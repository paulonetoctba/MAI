"""
MAI Strategic Agents

Base agent class and specialized agents for each strategic domain:
- Growth & Capital Efficiency Agent
- Performance Revenue Agent
- Funnel Economics Agent
- Behavioral & Demand Agent
- Market Sizing Agent
- Unit Economics / SaaS Agent
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List


class BaseAgent(ABC):
    """
    Base class for MAI strategic agents.
    
    Each agent specializes in a strategic domain and provides:
    - Domain-specific analysis
    - Relevant metrics identification
    - Strategic recommendations
    """
    
    def __init__(self, namespace: str):
        self.namespace = namespace
    
    @abstractmethod
    async def analyze(
        self,
        question: str,
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Perform domain-specific analysis"""
        pass
    
    @abstractmethod
    def get_metrics(self) -> List[str]:
        """Return relevant metrics for this domain"""
        pass
    
    @abstractmethod
    async def recommend(
        self,
        analysis: Dict[str, Any],
        context: Dict[str, Any],
    ) -> str:
        """Generate recommendation based on analysis"""
        pass


class GrowthCapitalAgent(BaseAgent):
    """Agent for Growth & Capital Efficiency analysis"""
    
    def __init__(self):
        super().__init__("growth_capital")
    
    async def analyze(
        self,
        question: str,
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Analyze growth and capital efficiency"""
        
        cac = context.get("cac", 0)
        ltv = context.get("ltv", 0)
        churn = context.get("churn_rate", 0)
        revenue = context.get("revenue_monthly", 0)
        
        # Calculate key metrics
        ltv_cac = ltv / cac if cac > 0 else 0
        cac_payback = cac / (revenue / 100) if revenue > 0 else 0  # Months
        
        return {
            "ltv_cac_ratio": round(ltv_cac, 2),
            "cac_payback_months": round(cac_payback, 1),
            "churn_rate": churn,
            "health": "healthy" if ltv_cac >= 3 else "at_risk" if ltv_cac >= 2 else "critical",
        }
    
    def get_metrics(self) -> List[str]:
        return ["CAC Payback", "LTV/CAC", "GEI", "Burn Multiple"]
    
    async def recommend(
        self,
        analysis: Dict[str, Any],
        context: Dict[str, Any],
    ) -> str:
        if analysis["health"] == "healthy":
            return "Fundamentos de growth sólidos. Escala pode ser considerada com monitoramento."
        elif analysis["health"] == "at_risk":
            return "Unit economics marginais. Validar retention antes de escalar aquisição."
        else:
            return "Unit economics quebrados. Pausar growth e focar em produto/retenção."


class PerformanceRevenueAgent(BaseAgent):
    """Agent for Performance Orientada a Receita"""
    
    def __init__(self):
        super().__init__("performance_revenue")
    
    async def analyze(
        self,
        question: str,
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Analyze performance and revenue alignment"""
        
        # Placeholder for real analysis
        return {
            "roas_incremental": 2.1,
            "contribution_margin": 0.35,
            "media_efficiency": "moderate",
        }
    
    def get_metrics(self) -> List[str]:
        return ["ROAS Incremental", "Contribution Margin", "Margem líquida pós-mídia"]
    
    async def recommend(
        self,
        analysis: Dict[str, Any],
        context: Dict[str, Any],
    ) -> str:
        if analysis["roas_incremental"] >= 3:
            return "Mídia eficiente. Considerar escala com controle."
        else:
            return "ROAS abaixo do ideal. Otimizar antes de escalar."


class FunnelEconomicsAgent(BaseAgent):
    """Agent for Funil & Economia da Conversão"""
    
    def __init__(self):
        super().__init__("funnel_economics")
    
    async def analyze(
        self,
        question: str,
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        return {
            "bottleneck": "consideration_to_trial",
            "financial_dropoff": 0.42,
            "optimizable": True,
        }
    
    def get_metrics(self) -> List[str]:
        return ["Custo por etapa", "Drop-off financeiro", "Win rate ajustado"]
    
    async def recommend(
        self,
        analysis: Dict[str, Any],
        context: Dict[str, Any],
    ) -> str:
        return f"Gargalo identificado: {analysis['bottleneck']}. Priorizar otimização."


class BehavioralDemandAgent(BaseAgent):
    """Agent for Psicologia & Demanda Econômica"""
    
    def __init__(self):
        super().__init__("behavioral_demand")
    
    async def analyze(
        self,
        question: str,
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        return {
            "price_elasticity": -1.2,
            "pricing_power": "moderate",
            "psychological_triggers": ["scarcity", "social_proof"],
        }
    
    def get_metrics(self) -> List[str]:
        return ["Elasticidade de preço", "Taxa de ativação", "Ticket médio"]
    
    async def recommend(
        self,
        analysis: Dict[str, Any],
        context: Dict[str, Any],
    ) -> str:
        return "Pricing power moderado. Testar aumento gradual com gatilhos comportamentais."


class MarketSizingAgent(BaseAgent):
    """Agent for Market Sizing & Expansão"""
    
    def __init__(self):
        super().__init__("market_sizing")
    
    async def analyze(
        self,
        question: str,
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        return {
            "tam": 1000000000,
            "sam": 100000000,
            "som": 10000000,
            "penetration": 0.02,
        }
    
    def get_metrics(self) -> List[str]:
        return ["TAM", "SAM", "SOM", "Penetração por segmento"]
    
    async def recommend(
        self,
        analysis: Dict[str, Any],
        context: Dict[str, Any],
    ) -> str:
        if analysis["penetration"] < 0.1:
            return "Baixa penetração no SOM. Foco em dominar segmento antes de expandir."
        else:
            return "Penetração sólida. Expansão adjacente pode ser considerada."


class UnitEconomicsAgent(BaseAgent):
    """Agent for Economia Unitária & SaaS"""
    
    def __init__(self):
        super().__init__("unit_economics")
    
    async def analyze(
        self,
        question: str,
        context: Dict[str, Any],
    ) -> Dict[str, Any]:
        churn = context.get("churn_rate", 0)
        gross_margin = context.get("gross_margin", 0.7)
        
        return {
            "gross_margin": gross_margin,
            "nrr": 1.05 if churn < 0.05 else 0.95,
            "revenue_churn": churn,
            "health": "healthy" if churn < 0.05 else "concerning",
        }
    
    def get_metrics(self) -> List[str]:
        return ["Gross Margin", "NRR", "Churn por receita", "CAC Payback"]
    
    async def recommend(
        self,
        analysis: Dict[str, Any],
        context: Dict[str, Any],
    ) -> str:
        if analysis["health"] == "healthy":
            return "Unit economics saudáveis. Modelo escalável."
        else:
            return "Churn preocupante. Priorizar retenção sobre crescimento."


# Agent registry
AGENTS = {
    "growth_capital": GrowthCapitalAgent,
    "performance_revenue": PerformanceRevenueAgent,
    "funnel_economics": FunnelEconomicsAgent,
    "behavioral_demand": BehavioralDemandAgent,
    "market_sizing": MarketSizingAgent,
    "unit_economics": UnitEconomicsAgent,
}


def get_agent(namespace: str) -> BaseAgent:
    """Get agent instance by namespace"""
    agent_class = AGENTS.get(namespace)
    if agent_class:
        return agent_class()
    raise ValueError(f"Unknown agent namespace: {namespace}")
