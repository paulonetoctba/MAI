"use client";

import React from "react";
import Link from "next/link";
import { Button } from "@/components/ui/Button";

export function CTA() {
    return (
        <section className="py-24 relative overflow-hidden">
            <div className="absolute inset-0 bg-dark-950"></div>

            {/* Background Effects */}
            <div className="absolute inset-0">
                <div className="absolute top-0 left-1/4 w-96 h-96 bg-mai-600/20 rounded-full blur-[150px]"></div>
                <div className="absolute bottom-0 right-1/4 w-80 h-80 bg-purple-600/20 rounded-full blur-[120px]"></div>
            </div>

            <div className="relative z-10 max-w-4xl mx-auto px-6 text-center">
                {/* Main CTA Card */}
                <div className="glass-strong rounded-3xl p-12 border border-mai-500/20">
                    <h2 className="text-3xl md:text-5xl font-bold text-white mb-6">
                        Pronto para tomar{" "}
                        <span className="gradient-text">decisões melhores?</span>
                    </h2>

                    <p className="text-dark-300 text-lg mb-8 max-w-2xl mx-auto">
                        A MAI existe para evitar decisões erradas antes que elas custem
                        caro. Comece agora e transforme como sua empresa faz marketing.
                    </p>

                    <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
                        <Link href="/auth/register">
                            <Button size="lg" className="min-w-[220px] animate-pulse-glow">
                                Criar Conta Grátis
                            </Button>
                        </Link>
                        <Link href="#como-funciona">
                            <Button variant="outline" size="lg" className="min-w-[220px]">
                                Agendar Demo
                            </Button>
                        </Link>
                    </div>

                    {/* Trust Badges */}
                    <div className="mt-10 pt-8 border-t border-dark-700">
                        <div className="flex flex-wrap items-center justify-center gap-8 text-dark-500 text-sm">
                            <div className="flex items-center gap-2">
                                <span className="text-mai-400">✓</span>
                                <span>Setup em 5 minutos</span>
                            </div>
                            <div className="flex items-center gap-2">
                                <span className="text-mai-400">✓</span>
                                <span>Sem cartão de crédito</span>
                            </div>
                            <div className="flex items-center gap-2">
                                <span className="text-mai-400">✓</span>
                                <span>Dados seguros</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    );
}
