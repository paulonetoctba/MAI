"use client";

import React from "react";
import { cn } from "@/lib/utils";

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
    variant?: "default" | "glass" | "gradient";
    hover?: boolean;
    children: React.ReactNode;
}

export function Card({
    variant = "default",
    hover = true,
    className,
    children,
    ...props
}: CardProps) {
    const variants = {
        default: "bg-dark-900/50 border border-dark-700",
        glass: "glass",
        gradient: "gradient-border",
    };

    const hoverStyles = hover
        ? "hover:border-mai-500/50 hover:shadow-lg hover:shadow-mai-500/10 transition-all duration-300"
        : "";

    return (
        <div
            className={cn(
                "rounded-2xl p-6",
                variants[variant],
                hoverStyles,
                className
            )}
            {...props}
        >
            {children}
        </div>
    );
}

export function CardHeader({
    className,
    children,
}: {
    className?: string;
    children: React.ReactNode;
}) {
    return <div className={cn("mb-4", className)}>{children}</div>;
}

export function CardTitle({
    className,
    children,
}: {
    className?: string;
    children: React.ReactNode;
}) {
    return (
        <h3 className={cn("text-xl font-semibold text-white", className)}>
            {children}
        </h3>
    );
}

export function CardDescription({
    className,
    children,
}: {
    className?: string;
    children: React.ReactNode;
}) {
    return (
        <p className={cn("text-dark-400 text-sm mt-1", className)}>{children}</p>
    );
}

export function CardContent({
    className,
    children,
}: {
    className?: string;
    children: React.ReactNode;
}) {
    return <div className={cn("", className)}>{children}</div>;
}
