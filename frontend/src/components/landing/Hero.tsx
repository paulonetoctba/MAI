"use client";

import React from "react";
import Link from "next/link";
import { Button } from "@/components/ui/Button";

export function Hero() {
    return (
        <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
            {/* Background Effects */}
            <div className="absolute inset-0 bg-hero-gradient"></div>
            <div className="absolute inset-0">
                <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-mai-600/20 rounded-full blur-[128px] animate-pulse"></div>
                <div className="absolute bottom-1/4 right-1/4 w-80 h-80 bg-purple-600/20 rounded-full blur-[128px] animate-pulse animation-delay-1000"></div>
                <div className="absolute top-1/2 right-1/3 w-64 h-64 bg-pink-600/10 rounded-full blur-[100px] animate-float"></div>
            </div>

            {/* Grid Pattern */}
            <div
                className="absolute inset-0 opacity-10"
                style={{
                    backgroundImage: `linear-gradient(rgba(99, 102, 241, 0.1) 1px, transparent 1px),
                            linear-gradient(90deg, rgba(99, 102, 241, 0.1) 1px, transparent 1px)`,
                    backgroundSize: "60px 60px",
                }}
            ></div>

            <div className="relative z-10 max-w-7xl mx-auto px-6 text-center pt-24">
                {/* Badge */}
                <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-mai-500/10 border border-mai-500/30 mb-8 animate-fade-in">
                    <span className="w-2 h-2 bg-mai-500 rounded-full animate-pulse"></span>
                    <span className="text-sm text-mai-300 font-medium">
                        Decision Intelligence para Marketing
                    </span>
                </div>

                {/* Main Headline */}
                <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold leading-tight mb-6 animate-slide-up">
                    <span className="text-white">Decisões de Marketing que</span>
                    <br />
                    <span className="gradient-text text-shadow-glow">
                        Protegem Caixa e Aceleram Crescimento
                    </span>
                </h1>

                {/* Subheadline */}
                <p className="text-lg md:text-xl text-dark-300 max-w-3xl mx-auto mb-10 animate-slide-up animate-delay-100">
                    A MAI é uma IA estratégica que analisa suas campanhas, identifica
                    riscos ocultos e recomenda decisões com impacto real no negócio.
                    <span className="text-white font-medium">
                        {" "}
                        Não é chatbot. É inteligência de decisão.
                    </span>
                </p>

                {/* CTA Buttons */}
                <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-16 animate-slide-up animate-delay-200">
                    <Link href="/auth/register">
                        <Button size="lg" className="min-w-[200px] animate-pulse-glow">
                            Começar Agora
                        </Button>
                    </Link>
                    <Link href="#como-funciona">
                        <Button variant="outline" size="lg" className="min-w-[200px]">
                            Ver Como Funciona
                        </Button>
                    </Link>
                </div>

                {/* Stats */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl mx-auto animate-fade-in animate-delay-300">
                    <div className="glass rounded-2xl p-6 text-center">
                        <div className="text-3xl font-bold gradient-text mb-2">+127%</div>
                        <div className="text-dark-400 text-sm">
                            Eficiência de Capital média
                        </div>
                    </div>
                    <div className="glass rounded-2xl p-6 text-center">
                        <div className="text-3xl font-bold gradient-text mb-2">-43%</div>
                        <div className="text-dark-400 text-sm">
                            Redução de decisões arriscadas
                        </div>
                    </div>
                    <div className="glass rounded-2xl p-6 text-center">
                        <div className="text-3xl font-bold gradient-text mb-2">2.4x</div>
                        <div className="text-dark-400 text-sm">
                            Retorno sobre investimento
                        </div>
                    </div>
                </div>
            </div>

            {/* Scroll Indicator */}
            <div className="absolute bottom-8 left-1/2 -translate-x-1/2 animate-bounce">
                <div className="w-6 h-10 border-2 border-dark-500 rounded-full flex items-start justify-center p-2">
                    <div className="w-1 h-2 bg-mai-500 rounded-full animate-pulse"></div>
                </div>
            </div>
        </section>
    );
}
