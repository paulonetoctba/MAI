"use client";

import { useState } from "react";
import {
    Brain,
    Send,
    History,
    AlertTriangle,
    CheckCircle,
    XCircle,
    Loader2,
    ChevronRight,
} from "lucide-react";

export default function DecisionsPage() {
    const [question, setQuestion] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const [result, setResult] = useState<any>(null);
    const [companyStage, setCompanyStage] = useState("scale");
    const [decisionType, setDecisionType] = useState("growth");

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!question.trim()) return;

        setIsLoading(true);

        // Simulate API call
        await new Promise((resolve) => setTimeout(resolve, 2000));

        setResult({
            diagnosis:
                "O LTV/CAC atual (2.5x) está abaixo do mínimo saudável (3x). Escalar aquisição agora pode acelerar a queima de caixa sem garantia de retorno.",
            key_metrics: ["CAC Payback", "LTV/CAC", "Churn por coorte", "Burn Multiple"],
            hidden_risks: [
                "Unit economics frágeis - risco de escala prematura",
                "Churn elevado indica problema de produto, não de aquisição",
                "Aumento de investimento pode elevar CAC (diminishing returns)",
            ],
            strategic_principle:
                "Eficiência de capital: crescer apenas quando unit economics comprovados",
            decision_score: {
                impact: 4,
                risk: 4,
                urgency: 3,
                score: 3.0,
                interpretation: "VALIDAR",
            },
            mai_decision: "AJUSTAR",
            next_step:
                "Ajustar escopo ou cronograma. Validar hipóteses com teste controlado antes de escala.",
            validation_verdict: "AJUSTAR",
        });

        setIsLoading(false);
    };

    const decisionHistory = [
        {
            id: "1",
            question: "Devemos escalar investimento em tráfego pago?",
            decision: "AJUSTAR",
            score: 4.2,
            date: "30 Jan 2026",
        },
        {
            id: "2",
            question: "Pausar campanha de awareness?",
            decision: "EXECUTAR",
            score: 6.5,
            date: "29 Jan 2026",
        },
        {
            id: "3",
            question: "Investir em TikTok Ads?",
            decision: "PAUSAR",
            score: 2.8,
            date: "28 Jan 2026",
        },
        {
            id: "4",
            question: "Aumentar budget de retargeting em 50%?",
            decision: "EXECUTAR",
            score: 7.2,
            date: "27 Jan 2026",
        },
    ];

    return (
        <div className="max-w-6xl mx-auto space-y-6">
            {/* Page Header */}
            <div>
                <h1 className="text-2xl font-bold text-white">Avaliação de Decisões</h1>
                <p className="text-gray-500">
                    Use o MAI para analisar decisões estratégicas de marketing
                </p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Main Form */}
                <div className="lg:col-span-2 space-y-6">
                    <form onSubmit={handleSubmit} className="p-6 rounded-2xl bg-dark-900 border border-white/5">
                        <div className="flex items-center gap-3 mb-6">
                            <div className="p-3 rounded-xl bg-mai-500/10">
                                <Brain size={24} className="text-mai-400" />
                            </div>
                            <div>
                                <h2 className="text-lg font-semibold text-white">Nova Decisão</h2>
                                <p className="text-sm text-gray-500">Descreva sua questão estratégica</p>
                            </div>
                        </div>

                        {/* Context selectors */}
                        <div className="grid grid-cols-2 gap-4 mb-4">
                            <div>
                                <label className="block text-sm text-gray-400 mb-2">Estágio da Empresa</label>
                                <select
                                    value={companyStage}
                                    onChange={(e) => setCompanyStage(e.target.value)}
                                    className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white text-sm focus:outline-none focus:border-mai-500/50"
                                >
                                    <option value="traction">Traction</option>
                                    <option value="scale">Scale</option>
                                    <option value="enterprise">Enterprise</option>
                                </select>
                            </div>
                            <div>
                                <label className="block text-sm text-gray-400 mb-2">Tipo de Decisão</label>
                                <select
                                    value={decisionType}
                                    onChange={(e) => setDecisionType(e.target.value)}
                                    className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white text-sm focus:outline-none focus:border-mai-500/50"
                                >
                                    <option value="growth">Growth</option>
                                    <option value="budget">Budget</option>
                                    <option value="product">Product</option>
                                    <option value="pricing">Pricing</option>
                                    <option value="market">Market</option>
                                </select>
                            </div>
                        </div>

                        {/* Question input */}
                        <textarea
                            value={question}
                            onChange={(e) => setQuestion(e.target.value)}
                            placeholder="Ex: Devemos escalar investimento em tráfego pago de R$50k para R$100k/mês?"
                            className="w-full h-32 px-4 py-3 bg-white/5 border border-white/10 rounded-xl text-white placeholder-gray-500 resize-none focus:outline-none focus:border-mai-500/50 transition-all"
                        />

                        <button
                            type="submit"
                            disabled={isLoading || !question.trim()}
                            className="mt-4 w-full flex items-center justify-center gap-2 py-3 bg-mai-500 hover:bg-mai-400 disabled:bg-mai-500/50 text-white rounded-xl font-semibold transition-colors"
                        >
                            {isLoading ? (
                                <>
                                    <Loader2 size={18} className="animate-spin" />
                                    Analisando...
                                </>
                            ) : (
                                <>
                                    <Send size={18} />
                                    Avaliar Decisão
                                </>
                            )}
                        </button>
                    </form>

                    {/* Result */}
                    {result && (
                        <div className="p-6 rounded-2xl bg-dark-900 border border-white/5 space-y-6">
                            {/* Decision Badge */}
                            <div className="flex items-center justify-between">
                                <h3 className="text-lg font-semibold text-white">Resultado da Análise</h3>
                                <DecisionBadge decision={result.mai_decision} />
                            </div>

                            {/* MAI Score */}
                            <div className="p-4 rounded-xl bg-white/5">
                                <div className="flex items-center justify-between mb-3">
                                    <span className="text-sm text-gray-400">MAI Decision Score™</span>
                                    <span className="text-2xl font-bold text-white">{result.decision_score.score}</span>
                                </div>
                                <div className="grid grid-cols-3 gap-4">
                                    <ScoreItem label="Impacto" value={result.decision_score.impact} />
                                    <ScoreItem label="Risco" value={result.decision_score.risk} />
                                    <ScoreItem label="Urgência" value={result.decision_score.urgency} />
                                </div>
                                <p className="mt-3 text-xs text-gray-500">
                                    Fórmula: (Impacto × Urgência) ÷ Risco
                                </p>
                            </div>

                            {/* Diagnosis */}
                            <div>
                                <h4 className="text-sm font-semibold text-white mb-2">Diagnóstico</h4>
                                <p className="text-sm text-gray-400 leading-relaxed">{result.diagnosis}</p>
                            </div>

                            {/* Key Metrics */}
                            <div>
                                <h4 className="text-sm font-semibold text-white mb-2">Métricas-Chave</h4>
                                <div className="flex flex-wrap gap-2">
                                    {result.key_metrics.map((metric: string) => (
                                        <span
                                            key={metric}
                                            className="px-3 py-1 bg-mai-500/10 text-mai-400 rounded-lg text-xs"
                                        >
                                            {metric}
                                        </span>
                                    ))}
                                </div>
                            </div>

                            {/* Hidden Risks */}
                            <div>
                                <h4 className="text-sm font-semibold text-white mb-2 flex items-center gap-2">
                                    <AlertTriangle size={14} className="text-yellow-400" />
                                    Riscos Ocultos
                                </h4>
                                <ul className="space-y-2">
                                    {result.hidden_risks.map((risk: string, i: number) => (
                                        <li key={i} className="flex items-start gap-2 text-sm text-gray-400">
                                            <span className="text-yellow-400">•</span>
                                            {risk}
                                        </li>
                                    ))}
                                </ul>
                            </div>

                            {/* Strategic Principle */}
                            <div className="p-4 rounded-xl bg-mai-500/5 border border-mai-500/20">
                                <h4 className="text-sm font-semibold text-mai-400 mb-1">Princípio Estratégico</h4>
                                <p className="text-sm text-gray-300">{result.strategic_principle}</p>
                            </div>

                            {/* Next Step */}
                            <div className="p-4 rounded-xl bg-green-500/5 border border-green-500/20">
                                <h4 className="text-sm font-semibold text-green-400 mb-1">Próximo Passo</h4>
                                <p className="text-sm text-gray-300">{result.next_step}</p>
                            </div>
                        </div>
                    )}
                </div>

                {/* History Sidebar */}
                <div className="p-6 rounded-2xl bg-dark-900 border border-white/5 h-fit">
                    <div className="flex items-center gap-2 mb-4">
                        <History size={18} className="text-gray-400" />
                        <h3 className="text-sm font-semibold text-white">Histórico</h3>
                    </div>
                    <div className="space-y-3">
                        {decisionHistory.map((item) => (
                            <div
                                key={item.id}
                                className="p-3 rounded-xl bg-white/5 hover:bg-white/10 cursor-pointer transition-colors group"
                            >
                                <p className="text-sm text-white line-clamp-2 mb-2">{item.question}</p>
                                <div className="flex items-center justify-between">
                                    <div className="flex items-center gap-2">
                                        <DecisionBadge decision={item.decision} small />
                                        <span className="text-xs text-gray-500">{item.score}</span>
                                    </div>
                                    <span className="text-xs text-gray-600">{item.date}</span>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
}

function DecisionBadge({ decision, small = false }: { decision: string; small?: boolean }) {
    const config = {
        EXECUTAR: { bg: "bg-green-500/10", text: "text-green-400", icon: CheckCircle },
        AJUSTAR: { bg: "bg-yellow-500/10", text: "text-yellow-400", icon: AlertTriangle },
        PAUSAR: { bg: "bg-red-500/10", text: "text-red-400", icon: XCircle },
        BLOQUEAR: { bg: "bg-red-500/10", text: "text-red-400", icon: XCircle },
    }[decision] || { bg: "bg-gray-500/10", text: "text-gray-400", icon: AlertTriangle };

    const Icon = config.icon;

    return (
        <span
            className={`inline-flex items-center gap-1 ${config.bg} ${config.text} ${small ? "px-2 py-0.5 text-xs" : "px-3 py-1 text-sm"
                } rounded-lg font-medium`}
        >
            <Icon size={small ? 12 : 14} />
            {decision}
        </span>
    );
}

function ScoreItem({ label, value }: { label: string; value: number }) {
    return (
        <div className="text-center">
            <p className="text-xs text-gray-500 mb-1">{label}</p>
            <p className="text-lg font-bold text-white">{value}</p>
        </div>
    );
}
