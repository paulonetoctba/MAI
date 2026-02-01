"use client";

import React from "react";

const beforeItems = [
    "Decisões baseadas em métricas de vaidade",
    "Escala sem validar eficiência",
    "Marketing desconectado do financeiro",
    "Riscos descobertos tarde demais",
    "Crescimento que queima caixa",
];

const afterItems = [
    "Decisões baseadas em impacto real",
    "Escala com eficiência de capital",
    "Marketing alinhado com receita",
    "Riscos identificados antecipadamente",
    "Crescimento sustentável e lucrativo",
];

export function BeforeAfter() {
    return (
        <section id="solucao" className="py-24 relative overflow-hidden">
            <div className="absolute inset-0 bg-dark-950"></div>

            {/* Background Accent */}
            <div className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-mai-600/10 rounded-full blur-[150px]"></div>

            <div className="relative z-10 max-w-7xl mx-auto px-6">
                {/* Section Header */}
                <div className="text-center mb-16">
                    <span className="text-mai-400 font-medium text-sm uppercase tracking-wider">
                        A Transformação
                    </span>
                    <h2 className="text-3xl md:text-5xl font-bold text-white mt-4 mb-6">
                        Antes vs Depois da <span className="gradient-text">MAI</span>
                    </h2>
                </div>

                {/* Comparison */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 lg:gap-4 items-stretch">
                    {/* Before */}
                    <div className="relative">
                        <div className="absolute inset-0 bg-gradient-to-br from-red-500/10 to-orange-500/10 rounded-3xl blur-xl"></div>
                        <div className="relative glass rounded-3xl p-8 h-full border-red-500/20">
                            <div className="flex items-center gap-3 mb-8">
                                <div className="w-12 h-12 rounded-xl bg-red-500/20 flex items-center justify-center">
                                    <span className="text-2xl">❌</span>
                                </div>
                                <div>
                                    <h3 className="text-xl font-bold text-white">Antes</h3>
                                    <p className="text-dark-400 text-sm">Sem a MAI</p>
                                </div>
                            </div>

                            <ul className="space-y-4">
                                {beforeItems.map((item, index) => (
                                    <li key={index} className="flex items-start gap-3">
                                        <div className="w-6 h-6 rounded-full bg-red-500/20 flex items-center justify-center flex-shrink-0 mt-0.5">
                                            <span className="text-red-400 text-sm">✕</span>
                                        </div>
                                        <span className="text-dark-300">{item}</span>
                                    </li>
                                ))}
                            </ul>
                        </div>
                    </div>

                    {/* After */}
                    <div className="relative">
                        <div className="absolute inset-0 bg-gradient-to-br from-mai-500/10 to-green-500/10 rounded-3xl blur-xl"></div>
                        <div className="relative glass rounded-3xl p-8 h-full border-mai-500/30">
                            <div className="flex items-center gap-3 mb-8">
                                <div className="w-12 h-12 rounded-xl bg-mai-500/20 flex items-center justify-center">
                                    <span className="text-2xl">✅</span>
                                </div>
                                <div>
                                    <h3 className="text-xl font-bold text-white">Depois</h3>
                                    <p className="text-dark-400 text-sm">Com a MAI</p>
                                </div>
                            </div>

                            <ul className="space-y-4">
                                {afterItems.map((item, index) => (
                                    <li key={index} className="flex items-start gap-3">
                                        <div className="w-6 h-6 rounded-full bg-mai-500/20 flex items-center justify-center flex-shrink-0 mt-0.5">
                                            <span className="text-mai-400 text-sm">✓</span>
                                        </div>
                                        <span className="text-white">{item}</span>
                                    </li>
                                ))}
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    );
}
