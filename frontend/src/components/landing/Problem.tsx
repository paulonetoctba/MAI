"use client";

import React from "react";
import { Card, CardContent } from "@/components/ui/Card";

const problems = [
    {
        icon: "💸",
        title: "Queima de Caixa Silenciosa",
        description:
            "Campanhas que parecem performar bem, mas destroem margem sem ninguém perceber até ser tarde demais.",
    },
    {
        icon: "📊",
        title: "Métricas de Vaidade",
        description:
            "Decisões baseadas em impressões, likes e cliques que não se traduzem em receita real ou crescimento sustentável.",
    },
    {
        icon: "🎲",
        title: "Decisões no Achismo",
        description:
            "Marketing operando no escuro, sem conexão com métricas financeiras que realmente importam para o negócio.",
    },
    {
        icon: "⚠️",
        title: "Crescimento Artificial",
        description:
            "Escalar aquisição sem validar retenção. Comprar volume sem entender unit economics. Receita que não se sustenta.",
    },
];

export function Problem() {
    return (
        <section id="problema" className="py-24 relative">
            <div className="absolute inset-0 bg-gradient-to-b from-dark-950 via-dark-900 to-dark-950"></div>

            <div className="relative z-10 max-w-7xl mx-auto px-6">
                {/* Section Header */}
                <div className="text-center mb-16">
                    <span className="text-mai-400 font-medium text-sm uppercase tracking-wider">
                        O Problema
                    </span>
                    <h2 className="text-3xl md:text-5xl font-bold text-white mt-4 mb-6">
                        Marketing sem Inteligência de Decisão
                        <br />
                        <span className="gradient-text">Custa Caro</span>
                    </h2>
                    <p className="text-dark-400 text-lg max-w-2xl mx-auto">
                        A maioria das empresas opera com decisões de marketing baseadas em
                        intuição, não em análise estratégica real.
                    </p>
                </div>

                {/* Problem Cards */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {problems.map((problem, index) => (
                        <Card
                            key={index}
                            variant="glass"
                            className="group cursor-default"
                            hover
                        >
                            <CardContent>
                                <div className="flex items-start gap-4">
                                    <div className="text-4xl group-hover:scale-110 transition-transform">
                                        {problem.icon}
                                    </div>
                                    <div>
                                        <h3 className="text-xl font-semibold text-white mb-2 group-hover:text-mai-300 transition-colors">
                                            {problem.title}
                                        </h3>
                                        <p className="text-dark-400 leading-relaxed">
                                            {problem.description}
                                        </p>
                                    </div>
                                </div>
                            </CardContent>
                        </Card>
                    ))}
                </div>

                {/* Bottom Statement */}
                <div className="mt-16 text-center">
                    <div className="inline-block glass-strong rounded-2xl p-8 max-w-3xl">
                        <p className="text-xl text-white font-medium">
                            &quot;Cada decisão errada em marketing não é apenas dinheiro
                            jogado fora.
                            <br />
                            <span className="gradient-text">
                                É caixa que nunca mais volta.
                            </span>
                            &quot;
                        </p>
                    </div>
                </div>
            </div>
        </section>
    );
}
