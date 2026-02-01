"use client";

import { useState } from "react";
import { User, Bell, Shield, Key, Building, Save, Loader2 } from "lucide-react";
import Link from "next/link";

export default function SettingsPage() {
    const [isSaving, setIsSaving] = useState(false);
    const [formData, setFormData] = useState({
        name: "Paulo Beber",
        email: "paulo@empresa.com",
        company: "Empresa LTDA",
        role: "Admin",
        notifications: {
            email: true,
            push: true,
            weekly: false,
        },
    });

    const handleSave = async () => {
        setIsSaving(true);
        await new Promise((resolve) => setTimeout(resolve, 1000));
        setIsSaving(false);
    };

    return (
        <div className="max-w-4xl mx-auto space-y-6">
            {/* Page Header */}
            <div>
                <h1 className="text-2xl font-bold text-white">Configurações</h1>
                <p className="text-gray-500">Gerencie sua conta e preferências</p>
            </div>

            {/* Settings Sections */}
            <div className="space-y-6">
                {/* Profile */}
                <section className="p-6 rounded-2xl bg-dark-900 border border-white/5">
                    <div className="flex items-center gap-3 mb-6">
                        <div className="p-2 rounded-lg bg-mai-500/10">
                            <User size={20} className="text-mai-400" />
                        </div>
                        <div>
                            <h2 className="text-lg font-semibold text-white">Perfil</h2>
                            <p className="text-sm text-gray-500">Informações básicas da conta</p>
                        </div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                            <label className="block text-sm text-gray-400 mb-2">Nome</label>
                            <input
                                type="text"
                                value={formData.name}
                                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                                className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:border-mai-500/50"
                            />
                        </div>
                        <div>
                            <label className="block text-sm text-gray-400 mb-2">Email</label>
                            <input
                                type="email"
                                value={formData.email}
                                disabled
                                className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-gray-500 cursor-not-allowed"
                            />
                        </div>
                        <div>
                            <label className="block text-sm text-gray-400 mb-2">Empresa</label>
                            <input
                                type="text"
                                value={formData.company}
                                onChange={(e) => setFormData({ ...formData, company: e.target.value })}
                                className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-white focus:outline-none focus:border-mai-500/50"
                            />
                        </div>
                        <div>
                            <label className="block text-sm text-gray-400 mb-2">Função</label>
                            <input
                                type="text"
                                value={formData.role}
                                disabled
                                className="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-gray-500 cursor-not-allowed"
                            />
                        </div>
                    </div>
                </section>

                {/* Notifications */}
                <section className="p-6 rounded-2xl bg-dark-900 border border-white/5">
                    <div className="flex items-center gap-3 mb-6">
                        <div className="p-2 rounded-lg bg-mai-500/10">
                            <Bell size={20} className="text-mai-400" />
                        </div>
                        <div>
                            <h2 className="text-lg font-semibold text-white">Notificações</h2>
                            <p className="text-sm text-gray-500">Preferências de comunicação</p>
                        </div>
                    </div>

                    <div className="space-y-4">
                        <ToggleItem
                            label="Notificações por Email"
                            description="Receba atualizações importantes por email"
                            checked={formData.notifications.email}
                            onChange={(checked) =>
                                setFormData({
                                    ...formData,
                                    notifications: { ...formData.notifications, email: checked },
                                })
                            }
                        />
                        <ToggleItem
                            label="Notificações Push"
                            description="Receba alertas em tempo real"
                            checked={formData.notifications.push}
                            onChange={(checked) =>
                                setFormData({
                                    ...formData,
                                    notifications: { ...formData.notifications, push: checked },
                                })
                            }
                        />
                        <ToggleItem
                            label="Relatório Semanal"
                            description="Resumo semanal das métricas"
                            checked={formData.notifications.weekly}
                            onChange={(checked) =>
                                setFormData({
                                    ...formData,
                                    notifications: { ...formData.notifications, weekly: checked },
                                })
                            }
                        />
                    </div>
                </section>

                {/* Security */}
                <section className="p-6 rounded-2xl bg-dark-900 border border-white/5">
                    <div className="flex items-center gap-3 mb-6">
                        <div className="p-2 rounded-lg bg-mai-500/10">
                            <Shield size={20} className="text-mai-400" />
                        </div>
                        <div>
                            <h2 className="text-lg font-semibold text-white">Segurança</h2>
                            <p className="text-sm text-gray-500">Senha e autenticação</p>
                        </div>
                    </div>

                    <div className="space-y-4">
                        <div className="flex items-center justify-between p-4 rounded-xl bg-white/5">
                            <div>
                                <p className="text-sm font-medium text-white">Alterar Senha</p>
                                <p className="text-xs text-gray-500">Última alteração: há 30 dias</p>
                            </div>
                            <button className="px-4 py-2 text-sm text-mai-400 hover:text-mai-300 border border-mai-500/30 rounded-lg transition-colors">
                                Alterar
                            </button>
                        </div>
                        <div className="flex items-center justify-between p-4 rounded-xl bg-white/5">
                            <div>
                                <p className="text-sm font-medium text-white">Autenticação 2FA</p>
                                <p className="text-xs text-gray-500">Adicione uma camada extra de segurança</p>
                            </div>
                            <button className="px-4 py-2 text-sm text-mai-400 hover:text-mai-300 border border-mai-500/30 rounded-lg transition-colors">
                                Configurar
                            </button>
                        </div>
                    </div>
                </section>

                {/* API Keys */}
                <section className="p-6 rounded-2xl bg-dark-900 border border-white/5">
                    <div className="flex items-center gap-3 mb-6">
                        <div className="p-2 rounded-lg bg-mai-500/10">
                            <Key size={20} className="text-mai-400" />
                        </div>
                        <div>
                            <h2 className="text-lg font-semibold text-white">API Keys</h2>
                            <p className="text-sm text-gray-500">Acesso programático à API do MAI</p>
                        </div>
                    </div>

                    <div className="p-4 rounded-xl bg-white/5 flex items-center justify-between">
                        <div>
                            <p className="text-sm font-medium text-white">Nenhuma API Key criada</p>
                            <p className="text-xs text-gray-500">Crie uma key para integrar com suas ferramentas</p>
                        </div>
                        <button className="px-4 py-2 text-sm bg-mai-500 hover:bg-mai-400 text-white rounded-lg transition-colors">
                            Criar API Key
                        </button>
                    </div>
                </section>

                {/* Integrations Link */}
                <Link
                    href="/dashboard/settings/integrations"
                    className="flex items-center justify-between p-6 rounded-2xl bg-dark-900 border border-white/5 hover:border-mai-500/30 transition-all group"
                >
                    <div className="flex items-center gap-3">
                        <div className="p-2 rounded-lg bg-mai-500/10">
                            <Building size={20} className="text-mai-400" />
                        </div>
                        <div>
                            <h2 className="text-lg font-semibold text-white group-hover:text-mai-400 transition-colors">
                                Integrações de Canais
                            </h2>
                            <p className="text-sm text-gray-500">
                                Conecte Google Ads, Meta Ads e TikTok Ads
                            </p>
                        </div>
                    </div>
                    <span className="text-gray-500 group-hover:text-mai-400 group-hover:translate-x-1 transition-all">
                        →
                    </span>
                </Link>
            </div>

            {/* Save Button */}
            <div className="flex justify-end">
                <button
                    onClick={handleSave}
                    disabled={isSaving}
                    className="flex items-center gap-2 px-6 py-3 bg-mai-500 hover:bg-mai-400 disabled:bg-mai-500/50 text-white rounded-xl font-semibold transition-colors"
                >
                    {isSaving ? (
                        <>
                            <Loader2 size={18} className="animate-spin" />
                            Salvando...
                        </>
                    ) : (
                        <>
                            <Save size={18} />
                            Salvar Alterações
                        </>
                    )}
                </button>
            </div>
        </div>
    );
}

function ToggleItem({
    label,
    description,
    checked,
    onChange,
}: {
    label: string;
    description: string;
    checked: boolean;
    onChange: (checked: boolean) => void;
}) {
    return (
        <div className="flex items-center justify-between p-4 rounded-xl bg-white/5">
            <div>
                <p className="text-sm font-medium text-white">{label}</p>
                <p className="text-xs text-gray-500">{description}</p>
            </div>
            <button
                onClick={() => onChange(!checked)}
                className={`relative w-12 h-6 rounded-full transition-colors ${checked ? "bg-mai-500" : "bg-gray-600"
                    }`}
            >
                <span
                    className={`absolute top-1 w-4 h-4 bg-white rounded-full transition-all ${checked ? "left-7" : "left-1"
                        }`}
                />
            </button>
        </div>
    );
}
