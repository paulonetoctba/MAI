from fastapi import APIRouter, Depends
from typing import List

from app.api.deps import get_current_verified_user
from app.models.user import User
from app.engine.rag_engine import RAGEngine

router = APIRouter()


# Knowledge namespaces
NAMESPACES = [
    {
        "id": "growth_capital",
        "name": "Growth & Capital Efficiency",
        "description": "Métricas de crescimento e eficiência de capital",
        "metrics": ["CAC Payback", "LTV/CAC", "GEI", "Burn Multiple"],
    },
    {
        "id": "performance_revenue",
        "name": "Performance Orientada a Receita",
        "description": "Eliminar métricas de vaidade e alinhar mídia à geração de caixa",
        "metrics": ["ROAS Incremental", "Contribution Margin", "Margem líquida pós-mídia"],
    },
    {
        "id": "funnel_economics",
        "name": "Funil & Economia da Conversão",
        "description": "Otimização de conversão com foco em impacto financeiro",
        "metrics": ["Custo por etapa", "Drop-off financeiro", "Win rate ajustado"],
    },
    {
        "id": "behavioral_demand",
        "name": "Psicologia & Demanda Econômica",
        "description": "Ativar demanda real usando princípios comportamentais",
        "metrics": ["Elasticidade de preço", "Taxa de ativação", "Aumento de ticket"],
    },
    {
        "id": "market_sizing",
        "name": "Market Sizing & Expansão",
        "description": "Evitar escala fora do mercado real",
        "metrics": ["TAM", "SAM", "SOM", "Penetração por segmento"],
    },
    {
        "id": "unit_economics",
        "name": "Economia Unitária & SaaS",
        "description": "Garantir crescimento sustentável",
        "metrics": ["Gross Margin", "NRR", "Churn por receita", "CAC Payback"],
    },
]


@router.get("/namespaces")
async def list_namespaces(
    current_user: User = Depends(get_current_verified_user),
):
    """List available RAG knowledge namespaces"""
    return NAMESPACES


@router.get("/namespaces/{namespace_id}")
async def get_namespace(
    namespace_id: str,
    current_user: User = Depends(get_current_verified_user),
):
    """Get details of a specific namespace"""
    
    for ns in NAMESPACES:
        if ns["id"] == namespace_id:
            return ns
    
    return {"error": "Namespace not found"}


@router.get("/namespaces/{namespace_id}/search")
async def search_namespace(
    namespace_id: str,
    query: str,
    limit: int = 5,
    current_user: User = Depends(get_current_verified_user),
):
    """Search within a specific knowledge namespace"""
    
    rag_engine = RAGEngine()
    
    results = await rag_engine.search(
        namespace=namespace_id,
        query=query,
        limit=limit,
    )
    
    return {
        "namespace": namespace_id,
        "query": query,
        "results": results,
    }


@router.get("/principles")
async def list_strategic_principles(
    current_user: User = Depends(get_current_verified_user),
):
    """List core strategic principles used by MAI"""
    
    return [
        {
            "id": "capital_efficiency",
            "name": "Capital Efficiency",
            "description": "Crescimento sustentável com uso eficiente de capital",
        },
        {
            "id": "retention_before_scale",
            "name": "Retenção antes de Escala",
            "description": "Tráfego não valida produto. Retenção valida produto.",
        },
        {
            "id": "real_metrics",
            "name": "Métricas de Impacto Real",
            "description": "Ignorar métricas de vaidade. Focar em CAC, LTV, churn, margem.",
        },
        {
            "id": "risk_assessment",
            "name": "Avaliação de Risco",
            "description": "Cada decisão deve considerar o risco de destruição de caixa.",
        },
        {
            "id": "market_validation",
            "name": "Validação de Mercado",
            "description": "Evitar escala fora do mercado real. TAM não é garantia.",
        },
    ]
