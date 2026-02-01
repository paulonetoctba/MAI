"use client";

import React, { useState } from "react";
import Link from "next/link";
import { LogoFull } from "@/components/ui/Logo";
import { Button } from "@/components/ui/Button";

export default function ForgotPasswordPage() {
    const [email, setEmail] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const [success, setSuccess] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError("");

        try {
            const response = await fetch("/api/auth/forgot-password", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email }),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || "Erro ao enviar email");
            }

            setSuccess(true);
        } catch (err) {
            setError(err instanceof Error ? err.message : "Erro ao enviar email");
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
                            <span className="text-3xl">📧</span>
                        </div>
                        <h1 className="text-2xl font-bold text-white mb-4">
                            Email enviado!
                        </h1>
                        <p className="text-dark-400 mb-8">
                            Se existe uma conta com o email <strong>{email}</strong>,
                            você receberá instruções para redefinir sua senha.
                        </p>
                        <Link href="/auth/login">
                            <Button className="w-full" size="lg">
                                Voltar para Login
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

                {/* Forgot Password Card */}
                <div className="glass-strong rounded-3xl p-8">
                    <div className="text-center mb-8">
                        <h1 className="text-2xl font-bold text-white mb-2">
                            Esqueceu sua senha?
                        </h1>
                        <p className="text-dark-400">
                            Digite seu email e enviaremos instruções para redefinir sua senha
                        </p>
                    </div>

                    {error && (
                        <div className="mb-6 p-4 rounded-xl bg-red-500/10 border border-red-500/30 text-red-400 text-sm">
                            {error}
                        </div>
                    )}

                    <form onSubmit={handleSubmit} className="space-y-6">
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

                        <Button
                            type="submit"
                            className="w-full"
                            size="lg"
                            disabled={loading}
                        >
                            {loading ? "Enviando..." : "Enviar instruções"}
                        </Button>
                    </form>

                    <div className="mt-8 text-center">
                        <Link
                            href="/auth/login"
                            className="text-mai-400 hover:text-mai-300 font-medium transition-colors"
                        >
                            ← Voltar para login
                        </Link>
                    </div>
                </div>
            </div>
        </div>
    );
}
