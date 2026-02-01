"use client";

import React from "react";

const useCases = [
    {
        role: "CMO / Head de Marketing",
        question: "Devo escalar investimento em tráfego pago?",
        answer:
            "A MAI analisa CAC payback, eficiência de canal e margem líquida para recomendar escala ou contenção.",
        color: "mai",
    },
    {
        role: "CEO / Founder",
        question: "Nosso crescimento é sustentável?",
        answer:
            "Diagnóstico de crescimento artificial vs saudável, baseado em unit economics e retenção real.",
        color: "purple",
    },
    {
        role: "CFO / Investidor",
        question: "O marketing está protegendo ou queimando caixa?",
        answer:
            "Análise de burn multiple, capital efficiency e retorno sobre investimento por canal.",
        color: "pink",
    },
    {
        role: "Growth Lead",
        question: "Qual canal devo priorizar agora?",
        answer:
            "Ranking de canais por ROI marginal, com simulação de cenários e risco de saturação.",
        color: "green",
    },
];

export function UseCases() {
    return (
        <section className="py-24 relative">
            <div className="absolute inset-0 bg-gradient-to-b from-dark-950 via-dark-900 to-dark-950"></div>

            <div className="relative z-10 max-w-7xl mx-auto px-6">
                {/* Section Header */}
                <div className="text-center mb-16">
                    <span className="text-mai-400 font-medium text-sm uppercase tracking-wider">
                        Casos de Uso
                    </span>
                    <h2 className="text-3xl md:text-5xl font-bold text-white mt-4 mb-6">
                        Decisões Reais que a{" "}
                        <span className="gradient-text">MAI</span> Resolve
                    </h2>
                    <p className="text-dark-400 text-lg max-w-2xl mx-auto">
                        De C-levels a líderes de growth, a MAI responde às perguntas que
                        definem o futuro do negócio.
                    </p>
                </div>

                {/* Use Cases */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {useCases.map((useCase, index) => (
                        <div
                            key={index}
                            className="glass rounded-2xl p-6 hover:border-mai-500/30 transition-all duration-300 group"
                        >
                            {/* Role Badge */}
                            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-mai-500/10 border border-mai-500/30 mb-4">
                                <span className="text-mai-400 text-sm font-medium">
                                    {useCase.role}
                                </span>
                            </div>

                            {/* Question */}
                            <h3 className="text-xl font-semibold text-white mb-3 group-hover:text-mai-300 transition-colors">
                                &quot;{useCase.question}&quot;
                            </h3>

                            {/* Answer */}
                            <p className="text-dark-400 leading-relaxed">
                                <span className="text-mai-400 font-medium">MAI:</span>{" "}
                                {useCase.answer}
                            </p>
                        </div>
                    ))}
                </div>
            </div>
        </section>
    );
}
