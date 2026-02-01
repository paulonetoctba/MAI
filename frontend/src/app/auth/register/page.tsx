"use client";

import React, { useState } from "react";
import Link from "next/link";
import { LogoFull } from "@/components/ui/Logo";
import { Button } from "@/components/ui/Button";

export default function RegisterPage() {
    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [company, setCompany] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const [success, setSuccess] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError("");

        if (password !== confirmPassword) {
            setError("As senhas não coincidem");
            setLoading(false);
            return;
        }

        if (password.length < 8) {
            setError("A senha deve ter pelo menos 8 caracteres");
            setLoading(false);
            return;
        }

        try {
            const response = await fetch("/api/auth/register", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ name, email, company, password }),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || "Erro ao criar conta");
            }

            setSuccess(true);
        } catch (err) {
            setError(err instanceof Error ? err.message : "Erro ao criar conta");
        } finally {
            setLoading(false);
        }
    };

    if (success) {
        return (
            <div className="min-h-screen bg-dark-950 flex items-center justify-center px-6 py-12">
                <div className="absolute inset-0">
                    <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-mai-600/10 rounded-full blur-[150px]"></div>
                </div>

                <div className="relative z-10 w-full max-w-md text-center">
                    <div className="glass-strong rounded-3xl p-8">
                        <div className="w-16 h-16 rounded-full bg-mai-500/20 flex items-center justify-center mx-auto mb-6">
                            <span className="text-3xl">✅</span>
                        </div>
                        <h1 className="text-2xl font-bold text-white mb-4">
                            Conta criada com sucesso!
                        </h1>
                        <p className="text-dark-400 mb-8">
                            Enviamos um email de confirmação para <strong>{email}</strong>.
                            Por favor, verifique sua caixa de entrada.
                        </p>
                        <Link href="/auth/login">
                            <Button className="w-full" size="lg">
                                Ir para Login
                            </Button>
                        </Link>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-dark-950 flex items-center justify-center px-6 py-12">
            {/* Background Effects */}
            <div className="absolute inset-0">
                <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-mai-600/10 rounded-full blur-[150px]"></div>
                <div className="absolute bottom-1/4 right-1/4 w-80 h-80 bg-purple-600/10 rounded-full blur-[120px]"></div>
            </div>

            <div className="relative z-10 w-full max-w-md">
                {/* Logo */}
                <div className="text-center mb-8">
                    <Link href="/">
                        <LogoFull className="inline-flex" />
                    </Link>
                </div>

                {/* Register Card */}
                <div className="glass-strong rounded-3xl p-8">
                    <div className="text-center mb-8">
                        <h1 className="text-2xl font-bold text-white mb-2">Criar conta</h1>
                        <p className="text-dark-400">
                            Comece a tomar decisões estratégicas hoje
                        </p>
                    </div>

                    {error && (
                        <div className="mb-6 p-4 rounded-xl bg-red-500/10 border border-red-500/30 text-red-400 text-sm">
                            {error}
                        </div>
                    )}

                    <form onSubmit={handleSubmit} className="space-y-5">
                        <div>
                            <label
                                htmlFor="name"
                                className="block text-sm font-medium text-dark-300 mb-2"
                            >
                                Nome completo
                            </label>
                            <input
                                id="name"
                                type="text"
                                value={name}
                                onChange={(e) => setName(e.target.value)}
                                required
                                className="w-full px-4 py-3 rounded-xl bg-dark-800/50 border border-dark-600 text-white placeholder-dark-500 focus:outline-none focus:border-mai-500 focus:ring-1 focus:ring-mai-500 transition-colors"
                                placeholder="João Silva"
                            />
                        </div>

                        <div>
                            <label
                                htmlFor="email"
                                className="block text-sm font-medium text-dark-300 mb-2"
                            >
                                Email
                            </label>
                            <input
                                id="email"
                                type="email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                required
                                className="w-full px-4 py-3 rounded-xl bg-dark-800/50 border border-dark-600 text-white placeholder-dark-500 focus:outline-none focus:border-mai-500 focus:ring-1 focus:ring-mai-500 transition-colors"
                                placeholder="seu@email.com"
                            />
                        </div>

                        <div>
                            <label
                                htmlFor="company"
                                className="block text-sm font-medium text-dark-300 mb-2"
                            >
                                Empresa
                            </label>
                            <input
                                id="company"
                                type="text"
                                value={company}
                                onChange={(e) => setCompany(e.target.value)}
                                required
                                className="w-full px-4 py-3 rounded-xl bg-dark-800/50 border border-dark-600 text-white placeholder-dark-500 focus:outline-none focus:border-mai-500 focus:ring-1 focus:ring-mai-500 transition-colors"
                                placeholder="Nome da empresa"
                            />
                        </div>

                        <div>
                            <label
                                htmlFor="password"
                                className="block text-sm font-medium text-dark-300 mb-2"
                            >
                                Senha
                            </label>
                            <input
                                id="password"
                                type="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                required
                                className="w-full px-4 py-3 rounded-xl bg-dark-800/50 border border-dark-600 text-white placeholder-dark-500 focus:outline-none focus:border-mai-500 focus:ring-1 focus:ring-mai-500 transition-colors"
                                placeholder="Min. 8 caracteres"
                            />
                        </div>

                        <div>
                            <label
                                htmlFor="confirmPassword"
                                className="block text-sm font-medium text-dark-300 mb-2"
                            >
                                Confirmar senha
                            </label>
                            <input
                                id="confirmPassword"
                                type="password"
                                value={confirmPassword}
                                onChange={(e) => setConfirmPassword(e.target.value)}
                                required
                                className="w-full px-4 py-3 rounded-xl bg-dark-800/50 border border-dark-600 text-white placeholder-dark-500 focus:outline-none focus:border-mai-500 focus:ring-1 focus:ring-mai-500 transition-colors"
                                placeholder="Repita a senha"
                            />
                        </div>

                        <Button
                            type="submit"
                            className="w-full"
                            size="lg"
                            disabled={loading}
                        >
                            {loading ? "Criando..." : "Criar conta"}
                        </Button>
                    </form>

                    <div className="mt-6 text-center">
                        <p className="text-dark-400">
                            Já tem uma conta?{" "}
                            <Link
                                href="/auth/login"
                                className="text-mai-400 hover:text-mai-300 font-medium transition-colors"
                            >
                                Entrar
                            </Link>
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
}
