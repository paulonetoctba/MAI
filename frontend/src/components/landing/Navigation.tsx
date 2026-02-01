"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { LogoFull } from "@/components/ui/Logo";
import { Button } from "@/components/ui/Button";

export function Navigation() {
    const [scrolled, setScrolled] = useState(false);

    useEffect(() => {
        const handleScroll = () => {
            setScrolled(window.scrollY > 20);
        };
        window.addEventListener("scroll", handleScroll);
        return () => window.removeEventListener("scroll", handleScroll);
    }, []);

    return (
        <nav
            className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${scrolled ? "glass-strong py-3" : "py-5"
                }`}
        >
            <div className="max-w-7xl mx-auto px-6 flex items-center justify-between">
                <LogoFull />

                <div className="hidden md:flex items-center gap-8">
                    <Link
                        href="#problema"
                        className="text-dark-300 hover:text-white transition-colors"
                    >
                        Problema
                    </Link>
                    <Link
                        href="#solucao"
                        className="text-dark-300 hover:text-white transition-colors"
                    >
                        Solução
                    </Link>
                    <Link
                        href="#como-funciona"
                        className="text-dark-300 hover:text-white transition-colors"
                    >
                        Como Funciona
                    </Link>
                    <Link
                        href="#beneficios"
                        className="text-dark-300 hover:text-white transition-colors"
                    >
                        Benefícios
                    </Link>
                </div>

                <div className="flex items-center gap-4">
                    <Link href="/auth/login">
                        <Button variant="ghost" size="sm">
                            Entrar
                        </Button>
                    </Link>
                    <Link href="/auth/register">
                        <Button variant="primary" size="sm">
                            Criar Conta
                        </Button>
                    </Link>
                </div>
            </div>
        </nav>
    );
}
