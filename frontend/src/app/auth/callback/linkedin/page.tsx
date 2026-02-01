"use client";

import { useEffect, useState } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import { Loader2, CheckCircle, XCircle } from "lucide-react";

export default function LinkedInCallbackPage() {
    const searchParams = useSearchParams();
    const router = useRouter();
    const [status, setStatus] = useState<"loading" | "success" | "error">("loading");
    const [message, setMessage] = useState("");

    useEffect(() => {
        const code = searchParams.get("code");
        const state = searchParams.get("state");
        const error = searchParams.get("error");

        if (error) {
            setStatus("error");
            setMessage("Autenticação cancelada ou falhou.");
            return;
        }

        if (code && state) {
            handleCallback(code, state);
        } else {
            setStatus("error");
            setMessage("Parâmetros de callback inválidos.");
        }
    }, [searchParams]);

    const handleCallback = async (code: string, state: string) => {
        try {
            const response = await fetch(
                `http://localhost:8000/api/v1/auth/linkedin/callback?code=${encodeURIComponent(code)}&state=${encodeURIComponent(state)}`
            );

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || "Erro na autenticação");
            }

            // Store tokens
            localStorage.setItem("token", data.access_token);
            localStorage.setItem("refresh_token", data.refresh_token);

            setStatus("success");
            setMessage("Login realizado com sucesso!");

            // Redirect to dashboard
            setTimeout(() => {
                router.push("/dashboard");
            }, 1500);
        } catch (err) {
            setStatus("error");
            setMessage(err instanceof Error ? err.message : "Erro na autenticação");
        }
    };

    return (
        <div className="min-h-screen bg-dark-950 flex items-center justify-center">
            <div className="text-center">
                {status === "loading" && (
                    <>
                        <Loader2 className="w-12 h-12 text-mai-500 animate-spin mx-auto mb-4" />
                        <p className="text-white text-lg">Autenticando com LinkedIn...</p>
                    </>
                )}

                {status === "success" && (
                    <>
                        <CheckCircle className="w-12 h-12 text-green-500 mx-auto mb-4" />
                        <p className="text-white text-lg">{message}</p>
                        <p className="text-gray-500 text-sm mt-2">Redirecionando...</p>
                    </>
                )}

                {status === "error" && (
                    <>
                        <XCircle className="w-12 h-12 text-red-500 mx-auto mb-4" />
                        <p className="text-white text-lg">{message}</p>
                        <button
                            onClick={() => router.push("/auth/login")}
                            className="mt-4 px-6 py-2 bg-mai-500 hover:bg-mai-400 text-white rounded-lg transition-colors"
                        >
                            Voltar ao Login
                        </button>
                    </>
                )}
            </div>
        </div>
    );
}
