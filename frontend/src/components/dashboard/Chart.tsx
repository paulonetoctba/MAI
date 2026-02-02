"use client";

import {
    LineChart,
    Line,
    AreaChart,
    Area,
    BarChart,
    Bar,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer,
    Legend,
} from "recharts";
import { cn } from "@/lib/utils";

interface ChartProps {
    data: any[];
    className?: string;
}

const CustomTooltip = ({ active, payload, label }: any) => {
    if (active && payload && payload.length) {
        return (
            <div className="bg-dark-800 border border-white/10 rounded-xl p-3 shadow-xl">
                <p className="text-xs text-gray-500 mb-2">{label}</p>
                {payload.map((entry: any, index: number) => (
                    <p key={index} className="text-sm font-medium" style={{ color: entry.color }}>
                        {entry.name}: {typeof entry.value === "number" ? entry.value.toLocaleString() : entry.value}
                    </p>
                ))}
            </div>
        );
    }
    return null;
};

export function PerformanceChart({ data, className }: ChartProps) {
    return (
        <div className={cn("p-6 rounded-2xl bg-dark-900 border border-white/5", className)}>
            <div className="flex items-center justify-between mb-6">
                <div>
                    <h3 className="text-lg font-semibold text-white">Performance</h3>
                    <p className="text-sm text-gray-500">Últimos 30 dias</p>
                </div>
                <div className="flex gap-4">
                    <ChartLegendItem color="#f59e0b" label="Spend" />
                    <ChartLegendItem color="#10B981" label="Revenue" />
                </div>
            </div>
            <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={data}>
                        <defs>
                            <linearGradient id="colorSpend" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor="#f59e0b" stopOpacity={0.3} />
                                <stop offset="95%" stopColor="#f59e0b" stopOpacity={0} />
                            </linearGradient>
                            <linearGradient id="colorRevenue" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor="#10B981" stopOpacity={0.3} />
                                <stop offset="95%" stopColor="#10B981" stopOpacity={0} />
                            </linearGradient>
                        </defs>
                        <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                        <XAxis
                            dataKey="date"
                            axisLine={false}
                            tickLine={false}
                            tick={{ fill: "#6B7280", fontSize: 12 }}
                        />
                        <YAxis
                            axisLine={false}
                            tickLine={false}
                            tick={{ fill: "#6B7280", fontSize: 12 }}
                            tickFormatter={(value) => `R$${(value / 1000).toFixed(0)}k`}
                        />
                        <Tooltip content={<CustomTooltip />} />
                        <Area
                            type="monotone"
                            dataKey="spend"
                            name="Spend"
                            stroke="#f59e0b"
                            strokeWidth={2}
                            fillOpacity={1}
                            fill="url(#colorSpend)"
                        />
                        <Area
                            type="monotone"
                            dataKey="revenue"
                            name="Revenue"
                            stroke="#10B981"
                            strokeWidth={2}
                            fillOpacity={1}
                            fill="url(#colorRevenue)"
                        />
                    </AreaChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
}

export function ConversionsChart({ data, className }: ChartProps) {
    return (
        <div className={cn("p-6 rounded-2xl bg-dark-900 border border-white/5", className)}>
            <div className="flex items-center justify-between mb-6">
                <div>
                    <h3 className="text-lg font-semibold text-white">Conversões por Canal</h3>
                    <p className="text-sm text-gray-500">Esta semana</p>
                </div>
            </div>
            <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={data} barGap={8}>
                        <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                        <XAxis
                            dataKey="channel"
                            axisLine={false}
                            tickLine={false}
                            tick={{ fill: "#6B7280", fontSize: 12 }}
                        />
                        <YAxis
                            axisLine={false}
                            tickLine={false}
                            tick={{ fill: "#6B7280", fontSize: 12 }}
                        />
                        <Tooltip content={<CustomTooltip />} />
                        <Bar
                            dataKey="conversions"
                            name="Conversões"
                            fill="#f59e0b"
                            radius={[4, 4, 0, 0]}
                        />
                    </BarChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
}

export function ROASChart({ data, className }: ChartProps) {
    return (
        <div className={cn("p-6 rounded-2xl bg-dark-900 border border-white/5", className)}>
            <div className="flex items-center justify-between mb-6">
                <div>
                    <h3 className="text-lg font-semibold text-white">ROAS por Campanha</h3>
                    <p className="text-sm text-gray-500">Top 5 campanhas</p>
                </div>
            </div>
            <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={data} layout="vertical" barGap={8}>
                        <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" horizontal={false} />
                        <XAxis
                            type="number"
                            axisLine={false}
                            tickLine={false}
                            tick={{ fill: "#6B7280", fontSize: 12 }}
                            tickFormatter={(value) => `${value}x`}
                        />
                        <YAxis
                            type="category"
                            dataKey="campaign"
                            axisLine={false}
                            tickLine={false}
                            tick={{ fill: "#6B7280", fontSize: 12 }}
                            width={100}
                        />
                        <Tooltip content={<CustomTooltip />} />
                        <Bar
                            dataKey="roas"
                            name="ROAS"
                            fill="#10B981"
                            radius={[0, 4, 4, 0]}
                        />
                    </BarChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
}

function ChartLegendItem({ color, label }: { color: string; label: string }) {
    return (
        <div className="flex items-center gap-2">
            <div className="w-3 h-3 rounded-full" style={{ backgroundColor: color }} />
            <span className="text-xs text-gray-500">{label}</span>
        </div>
    );
}
