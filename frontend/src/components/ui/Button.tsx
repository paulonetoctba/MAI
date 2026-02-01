import React from "react";
import { cn } from "@/lib/utils";

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
    variant?: "primary" | "secondary" | "outline" | "ghost";
    size?: "sm" | "md" | "lg";
    children: React.ReactNode;
}

export function Button({
    variant = "primary",
    size = "md",
    className,
    children,
    ...props
}: ButtonProps) {
    const baseStyles =
        "inline-flex items-center justify-center font-semibold rounded-xl transition-all duration-300 focus:outline-none focus:ring-2 focus:ring-mai-500 focus:ring-offset-2 focus:ring-offset-dark-950 disabled:opacity-50 disabled:cursor-not-allowed";

    const variants = {
        primary:
            "bg-gradient-to-r from-mai-600 to-mai-500 text-white hover:from-mai-500 hover:to-mai-400 shadow-lg shadow-mai-500/25 hover:shadow-mai-500/40",
        secondary:
            "bg-dark-800 text-white hover:bg-dark-700 border border-dark-600",
        outline:
            "border-2 border-mai-500 text-mai-400 hover:bg-mai-500/10 hover:text-mai-300",
        ghost: "text-dark-300 hover:text-white hover:bg-dark-800",
    };

    const sizes = {
        sm: "text-sm px-4 py-2",
        md: "text-base px-6 py-3",
        lg: "text-lg px-8 py-4",
    };

    return (
        <button
            className={cn(baseStyles, variants[variant], sizes[size], className)}
            {...props}
        >
            {children}
        </button>
    );
}
