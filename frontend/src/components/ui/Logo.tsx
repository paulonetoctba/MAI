import React from "react";

interface LogoProps {
    className?: string;
    size?: "sm" | "md" | "lg" | "xl";
}

export function Logo({ className = "", size = "md" }: LogoProps) {
    const sizes = {
        sm: "text-xl",
        md: "text-2xl",
        lg: "text-4xl",
        xl: "text-6xl",
    };

    return (
        <div className={`font-bold tracking-tight ${sizes[size]} ${className}`}>
            <span className="text-white">M</span>
            <span className="gradient-text">AI</span>
        </div>
    );
}

export function LogoFull({ className = "" }: { className?: string }) {
    return (
        <div className={`flex items-center gap-3 ${className}`}>
            <div className="relative">
                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-mai-400 to-mai-600 flex items-center justify-center shadow-lg shadow-mai-500/30">
                    <span className="text-white font-bold text-lg">M</span>
                </div>
                <div className="absolute -inset-1 rounded-xl bg-gradient-to-br from-mai-300 to-mai-500 opacity-30 blur-sm -z-10"></div>
            </div>
            <div className="flex flex-col">
                <span className="text-xl font-bold text-white tracking-tight">MAI</span>
                <span className="text-[10px] text-dark-400 tracking-widest uppercase">
                    Marketing AI
                </span>
            </div>
        </div>
    );
}
