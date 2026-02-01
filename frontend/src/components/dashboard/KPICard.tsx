import { cn } from "@/lib/utils";
import { TrendingUp, TrendingDown, Minus } from "lucide-react";

interface KPICardProps {
    title: string;
    value: string;
    change?: number;
    changeLabel?: string;
    icon?: React.ElementType;
    className?: string;
}

export function KPICard({
    title,
    value,
    change,
    changeLabel = "vs. período anterior",
    icon: Icon,
    className,
}: KPICardProps) {
    const isPositive = change && change > 0;
    const isNegative = change && change < 0;
    const isNeutral = change === 0;

    return (
        <div
            className={cn(
                "p-6 rounded-2xl bg-dark-900 border border-white/5 hover:border-white/10 transition-all duration-300",
                className
            )}
        >
            <div className="flex items-start justify-between">
                <div>
                    <p className="text-sm text-gray-500 mb-1">{title}</p>
                    <p className="text-3xl font-bold text-white">{value}</p>
                </div>
                {Icon && (
                    <div className="p-3 rounded-xl bg-mai-500/10">
                        <Icon size={24} className="text-mai-400" />
                    </div>
                )}
            </div>

            {change !== undefined && (
                <div className="mt-4 flex items-center gap-2">
                    <span
                        className={cn(
                            "flex items-center gap-1 px-2 py-1 rounded-lg text-xs font-medium",
                            isPositive && "bg-green-500/10 text-green-400",
                            isNegative && "bg-red-500/10 text-red-400",
                            isNeutral && "bg-gray-500/10 text-gray-400"
                        )}
                    >
                        {isPositive && <TrendingUp size={12} />}
                        {isNegative && <TrendingDown size={12} />}
                        {isNeutral && <Minus size={12} />}
                        {isPositive && "+"}
                        {change}%
                    </span>
                    <span className="text-xs text-gray-600">{changeLabel}</span>
                </div>
            )}
        </div>
    );
}
