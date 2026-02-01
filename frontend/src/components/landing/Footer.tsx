import React from "react";
import Link from "next/link";
import { LogoFull } from "@/components/ui/Logo";

export function Footer() {
    return (
        <footer className="py-12 border-t border-dark-800 bg-dark-950">
            <div className="max-w-7xl mx-auto px-6">
                <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-12">
                    {/* Brand */}
                    <div className="md:col-span-2">
                        <LogoFull className="mb-4" />
                        <p className="text-dark-400 max-w-md">
                            Decision Intelligence para Marketing. A MAI ajuda empresas a tomar
                            decisões estratégicas que protegem caixa e aceleram crescimento.
                        </p>
                    </div>

                    {/* Links */}
                    <div>
                        <h4 className="text-white font-semibold mb-4">Produto</h4>
                        <ul className="space-y-2">
                            <li>
                                <Link
                                    href="#como-funciona"
                                    className="text-dark-400 hover:text-white transition-colors"
                                >
                                    Como Funciona
                                </Link>
                            </li>
                            <li>
                                <Link
                                    href="#beneficios"
                                    className="text-dark-400 hover:text-white transition-colors"
                                >
                                    Benefícios
                                </Link>
                            </li>
                            <li>
                                <Link
                                    href="#"
                                    className="text-dark-400 hover:text-white transition-colors"
                                >
                                    Preços
                                </Link>
                            </li>
                            <li>
                                <Link
                                    href="#"
                                    className="text-dark-400 hover:text-white transition-colors"
                                >
                                    API Docs
                                </Link>
                            </li>
                        </ul>
                    </div>

                    {/* Company */}
                    <div>
                        <h4 className="text-white font-semibold mb-4">Empresa</h4>
                        <ul className="space-y-2">
                            <li>
                                <Link
                                    href="#"
                                    className="text-dark-400 hover:text-white transition-colors"
                                >
                                    Sobre
                                </Link>
                            </li>
                            <li>
                                <Link
                                    href="#"
                                    className="text-dark-400 hover:text-white transition-colors"
                                >
                                    Blog
                                </Link>
                            </li>
                            <li>
                                <Link
                                    href="#"
                                    className="text-dark-400 hover:text-white transition-colors"
                                >
                                    Contato
                                </Link>
                            </li>
                            <li>
                                <Link
                                    href="#"
                                    className="text-dark-400 hover:text-white transition-colors"
                                >
                                    Carreiras
                                </Link>
                            </li>
                        </ul>
                    </div>
                </div>

                {/* Bottom */}
                <div className="pt-8 border-t border-dark-800 flex flex-col md:flex-row items-center justify-between gap-4">
                    <p className="text-dark-500 text-sm">
                        © {new Date().getFullYear()} MAI - Marketing Artificial
                        Intelligence. Todos os direitos reservados.
                    </p>
                    <div className="flex items-center gap-6 text-sm">
                        <Link
                            href="#"
                            className="text-dark-500 hover:text-white transition-colors"
                        >
                            Privacidade
                        </Link>
                        <Link
                            href="#"
                            className="text-dark-500 hover:text-white transition-colors"
                        >
                            Termos
                        </Link>
                    </div>
                </div>
            </div>
        </footer>
    );
}
