"use client";

import { DollarSign, TrendingUp, Users, Target, Brain, ArrowRight } from "lucide-react";
import { KPICard } from "@/components/dashboard/KPICard";
import { PerformanceChart, ConversionsChart, ROASChart } from "@/components/dashboard/Chart";
import Link from "next/link";

// Demo data
const performanceData = [
    { date: "01/01", spend: 12000, revenue: 36000 },
    { date: "05/01", spend: 15000, revenue: 42000 },
    { date: "10/01", spend: 14000, revenue: 38000 },
    { date: "15/01", spend: 18000, revenue: 52000 },
    { date: "20/01", spend: 22000, revenue: 58000 },
    { date: "25/01", spend: 19000, revenue: 48000 },
    { date: "30/01", spend: 21000, revenue: 62000 },
];

const conversionsData = [
    { channel: "Google", conversions: 245 },
    { channel: "Meta", conversions: 189 },
    { channel: "TikTok", conversions: 124 },
    { channel: "LinkedIn", conversions: 67 },
];

const roasData = [
    { campaign: "Brand Search", roas: 4.2 },
    { campaign: "Retargeting", roas: 3.8 },
    { campaign: "Lookalike", roas: 2.9 },
    { campaign: "Prospecting", roas: 2.1 },
    { campaign: "Display", roas: 1.4 },
];

const recentDecisions = [
    {
        id: "1",
        question: "Devemos escalar investimento em tráfego pago?",
        decision: "AJUSTAR",
        score: 4.2,
        date: "30 Jan",
    },
    {
        id: "2",
        question: "Pausar campanha de awareness?",
        decision: "EXECUTAR",
        score: 6.5,
        date: "29 Jan",
    },
    {
        id: "3",
        question: "Investir em TikTok Ads?",
        decision: "PAUSAR",
        score: 2.8,
        date: "28 Jan",
    },
];

export default function DashboardPage() {
    return (
        <div className="space-y-6">
            {/* Page Header */}
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-2xl font-bold text-white">Dashboard</h1>
                    <p className="text-gray-500">Visão geral das suas métricas e decisões</p>
                </div>
                <Link
                    href="/dashboard/decisions"
                    className="flex items-center gap-2 px-4 py-2.5 bg-mai-500 hover:bg-mai-400 text-white rounded-xl font-medium transition-colors"
                >
                    <Brain size={18} />
                    Nova Decisão
                </Link>
            </div>

            {/* KPI Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <KPICard
                    title="Total Spend"
                    value="R$ 121.5k"
                    change={12.5}
                    icon={DollarSign}
                />
                <KPICard
                    title="ROAS Médio"
                    value="2.9x"
                    change={-5.2}
                    icon={TrendingUp}
                />
                <KPICard
                    title="Conversões"
                    value="625"
                    change={8.3}
                    icon={Users}
                />
                <KPICard
                    title="CAC"
                    value="R$ 194"
                    change={-3.1}
                    icon={Target}
                />
            </div>

            {/* Charts Row */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <PerformanceChart data={performanceData} />
                <ConversionsChart data={conversionsData} />
            </div>

            {/* Bottom Row */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <ROASChart data={roasData} className="lg:col-span-2" />

                {/* Recent Decisions */}
                <div className="p-7.5 rounded-sm bg-white border border-gray-200 shadow-default">
                    <div className="flex items-center justify-between mb-6">
                        <h3 className="text-lg font-semibold text-black">Decisões Recentes</h3>
                        <Link
                            href="/dashboard/decisions"
                            className="text-sm text-mai-400 hover:text-mai-300 transition-colors"
                        >
                            Ver todas
                        </Link>
                    </div>
                    <div className="space-y-3">
                        {recentDecisions.map((decision) => (
                            <div
                                key={decision.id}
                                className="p-4 rounded-xl bg-white/5 hover:bg-white/10 transition-colors cursor-pointer"
                            >
                                <div className="flex items-start justify-between mb-2">
                                    <p className="text-sm text-black line-clamp-1 flex-1 font-medium">
                                        {decision.question}
                                    </p>
                                    <span
                                        className={`ml-2 px-2 py-0.5 rounded text-xs font-medium ${decision.decision === "EXECUTAR"
                                            ? "bg-green-500/10 text-green-400"
                                            : decision.decision === "AJUSTAR"
                                                ? "bg-yellow-500/10 text-yellow-400"
                                                : "bg-red-500/10 text-red-400"
                                            }`}
                                    >
                                        {decision.decision}
                                    </span>
                                </div>
                                <div className="flex items-center justify-between">
                                    <span className="text-xs text-gray-500">
                                        Score: {decision.score}
                                    </span>
                                    <span className="text-xs text-gray-600">{decision.date}</span>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>

            {/* Quick Actions */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <QuickAction
                    title="Avaliar Decisão"
                    description="Use o MAI para analisar uma decisão estratégica"
                    href="/dashboard/decisions"
                    icon={Brain}
                />
                <QuickAction
                    title="Sincronizar Dados"
                    description="Atualize dados das plataformas de ads"
                    href="/dashboard/settings/integrations"
                    icon={TrendingUp}
                />
                <QuickAction
                    title="Ver Campanhas"
                    description="Analise performance das campanhas"
                    href="/dashboard/campaigns"
                    icon={Target}
                />
            </div>
        </div>
    );
}

function QuickAction({
    title,
    description,
    href,
    icon: Icon,
}: {
    title: string;
    description: string;
    href: string;
    icon: React.ElementType;
}) {
    return (
        <Link
            href={href}
            className="group p-7.5 rounded-sm bg-white border border-gray-200 shadow-default hover:border-mai-500/30 transition-all duration-300"
        >
            <div className="flex items-center gap-4">
                <div className="p-3 rounded-xl bg-mai-500/10 group-hover:bg-mai-500/20 transition-colors">
                    <Icon size={24} className="text-mai-400" />
                </div>
                <div className="flex-1">
                    <h4 className="text-sm font-semibold text-black group-hover:text-mai-500 transition-colors">
                        {title}
                    </h4>
                    <p className="text-xs text-gray-500">{description}</p>
                </div>
                <ArrowRight
                    size={18}
                    className="text-gray-600 group-hover:text-mai-400 group-hover:translate-x-1 transition-all"
                />
            </div>
        </Link>
    );
}
