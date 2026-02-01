"use client";

import React from "react";

const steps = [
    {
        number: "01",
        title: "Conecte Seus Dados",
        description:
            "Integração direta com Google Ads, Meta Ads e suas métricas de negócio. Dados em tempo real alimentando decisões inteligentes.",
        icon: "🔗",
    },
    {
        number: "02",
        title: "Diagnóstico Estratégico",
        description:
            "A MAI analisa suas campanhas, cruza com métricas financeiras (CAC, LTV, Churn) e identifica o problema real por trás dos números.",
        icon: "🔍",
    },
    {
        number: "03",
        title: "MAI Decision Score™",
        description:
            "Cada decisão é avaliada com um score baseado em Impacto × Urgência ÷ Risco. Sem achismo, sem viés.",
        icon: "📐",
    },
    {
        number: "04",
        title: "Validação Cruzada",
        description:
            "Uma segunda camada estratégica testa a robustez da recomendação, identificando falhas e riscos ocultos.",
        icon: "🛡️",
    },
    {
        number: "05",
        title: "Decisão Acionável",
        description:
            "Você recebe: diagnóstico claro, riscos mapeados, decisão recomendada (EXECUTAR / AJUSTAR / PAUSAR) e próximo passo concreto.",
        icon: "🎯",
    },
];

export function HowItWorks() {
    return (
        <section id="como-funciona" className="py-24 relative">
            <div className="absolute inset-0 bg-gradient-to-b from-dark-950 via-dark-900/50 to-dark-950"></div>

            <div className="relative z-10 max-w-7xl mx-auto px-6">
                {/* Section Header */}
                <div className="text-center mb-16">
                    <span className="text-mai-400 font-medium text-sm uppercase tracking-wider">
                        Como Funciona
                    </span>
                    <h2 className="text-3xl md:text-5xl font-bold text-white mt-4 mb-6">
                        O Motor Estratégico da{" "}
                        <span className="gradient-text">MAI</span>
                    </h2>
                    <p className="text-dark-400 text-lg max-w-2xl mx-auto">
                        Da entrada de dados até a decisão final, cada etapa foi projetada
                        para evitar erros caros antes que eles aconteçam.
                    </p>
                </div>

                {/* Steps */}
                <div className="relative">
                    {/* Connection Line */}
                    <div className="absolute left-8 md:left-1/2 top-0 bottom-0 w-px bg-gradient-to-b from-mai-500/50 via-mai-500/20 to-transparent hidden md:block"></div>

                    <div className="space-y-12">
                        {steps.map((step, index) => (
                            <div
                                key={index}
                                className={`relative flex flex-col md:flex-row items-start gap-8 ${index % 2 === 0 ? "md:flex-row" : "md:flex-row-reverse"
                                    }`}
                            >
                                {/* Step Content */}
                                <div
                                    className={`flex-1 ${index % 2 === 0 ? "md:text-right" : "md:text-left"
                                        }`}
                                >
                                    <div
                                        className={`glass rounded-2xl p-6 inline-block max-w-md ${index % 2 === 0 ? "md:ml-auto" : "md:mr-auto"
                                            }`}
                                    >
                                        <div
                                            className={`flex items-center gap-3 mb-4 ${index % 2 === 0
                                                    ? "md:flex-row-reverse"
                                                    : "md:flex-row"
                                                }`}
                                        >
                                            <span className="text-3xl">{step.icon}</span>
                                            <div>
                                                <span className="text-mai-400 text-sm font-mono">
                                                    {step.number}
                                                </span>
                                                <h3 className="text-xl font-semibold text-white">
                                                    {step.title}
                                                </h3>
                                            </div>
                                        </div>
                                        <p className="text-dark-400 leading-relaxed text-left">
                                            {step.description}
                                        </p>
                                    </div>
                                </div>

                                {/* Center Circle */}
                                <div className="hidden md:flex items-center justify-center w-16 flex-shrink-0">
                                    <div className="w-12 h-12 rounded-full bg-mai-500/20 border-2 border-mai-500 flex items-center justify-center">
                                        <span className="text-mai-400 font-bold text-sm">
                                            {step.number}
                                        </span>
                                    </div>
                                </div>

                                {/* Spacer */}
                                <div className="flex-1 hidden md:block"></div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </section>
    );
}
