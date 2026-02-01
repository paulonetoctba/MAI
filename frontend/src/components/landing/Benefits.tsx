"use client";

import React from "react";
import { Card, CardContent } from "@/components/ui/Card";

const benefits = [
    {
        icon: "🛡️",
        title: "Proteção de Caixa",
        description:
            "Identifique decisões que destroem margem antes de executá-las. Cada real investido é validado.",
    },
    {
        icon: "📈",
        title: "Crescimento Sustentável",
        description:
            "Escale apenas quando a eficiência estiver comprovada. Crescimento real, não artificialmente inflado.",
    },
    {
        icon: "🎯",
        title: "Decisões Explicáveis",
        description:
            "Cada recomendação vem com diagnóstico, métricas e score determinístico. Auditável e transparente.",
    },
    {
        icon: "⚡",
        title: "Velocidade Estratégica",
        description:
            "Análises que levariam dias são entregues em segundos. Time-to-decision drasticamente reduzido.",
    },
    {
        icon: "🔗",
        title: "Dados Integrados",
        description:
            "Google Ads, Meta Ads e suas métricas de negócio em um só lugar. Visão unificada do que importa.",
    },
    {
        icon: "🧠",
        title: "Inteligência Proprietária",
        description:
            "RAG treinado em princípios de growth, capital efficiency e economia comportamental.",
    },
];

export function Benefits() {
    return (
        <section id="beneficios" className="py-24 relative">
            <div className="absolute inset-0 bg-dark-950"></div>

            {/* Background Accents */}
            <div className="absolute right-0 top-1/4 w-96 h-96 bg-mai-600/10 rounded-full blur-[150px]"></div>
            <div className="absolute left-0 bottom-1/4 w-80 h-80 bg-purple-600/10 rounded-full blur-[120px]"></div>

            <div className="relative z-10 max-w-7xl mx-auto px-6">
                {/* Section Header */}
                <div className="text-center mb-16">
                    <span className="text-mai-400 font-medium text-sm uppercase tracking-wider">
                        Benefícios
                    </span>
                    <h2 className="text-3xl md:text-5xl font-bold text-white mt-4 mb-6">
                        Por Que Líderes Escolhem a{" "}
                        <span className="gradient-text">MAI</span>
                    </h2>
                    <p className="text-dark-400 text-lg max-w-2xl mx-auto">
                        Construída para executivos que não podem errar em decisões de
                        marketing e crescimento.
                    </p>
                </div>

                {/* Benefits Grid */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {benefits.map((benefit, index) => (
                        <Card key={index} variant="glass" hover className="group">
                            <CardContent>
                                <div className="w-14 h-14 rounded-2xl bg-mai-500/10 flex items-center justify-center mb-4 group-hover:bg-mai-500/20 transition-colors">
                                    <span className="text-3xl">{benefit.icon}</span>
                                </div>
                                <h3 className="text-xl font-semibold text-white mb-2 group-hover:text-mai-300 transition-colors">
                                    {benefit.title}
                                </h3>
                                <p className="text-dark-400 leading-relaxed">
                                    {benefit.description}
                                </p>
                            </CardContent>
                        </Card>
                    ))}
                </div>
            </div>
        </section>
    );
}
