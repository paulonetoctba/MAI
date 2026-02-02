"use client";

import { useState } from "react";
import { Search, Bell, User, ChevronDown } from "lucide-react";

export function Header() {
    const [showNotifications, setShowNotifications] = useState(false);
    const [showProfile, setShowProfile] = useState(false);

    return (
        <header className="h-16 bg-dark-900/80 backdrop-blur-xl border-b border-white/5 flex items-center justify-between px-6 sticky top-0 z-30">
            {/* Search */}
            <div className="relative w-96">
                <Search
                    size={18}
                    className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500"
                />
                <input
                    type="text"
                    placeholder="Buscar decisões, campanhas..."
                    className="w-full pl-10 pr-4 py-2.5 bg-white/5 border border-white/10 rounded-xl text-sm text-white placeholder-gray-500 focus:outline-none focus:border-mai-500/50 focus:ring-1 focus:ring-mai-500/50 transition-all font-medium"
                />
                <kbd className="absolute right-3 top-1/2 -translate-y-1/2 px-2 py-0.5 bg-white/10 rounded text-xs text-gray-500 border border-white/5">
                    ⌘K
                </kbd>
            </div>

            {/* Right Side */}
            <div className="flex items-center gap-4">
                {/* Notifications */}
                <div className="relative">
                    <button
                        onClick={() => setShowNotifications(!showNotifications)}
                        className="relative p-2.5 rounded-xl bg-white/5 hover:bg-white/10 transition-colors border border-white/5"
                    >
                        <Bell size={18} className="text-gray-400" />
                        <span className="absolute top-1.5 right-1.5 w-2 h-2 bg-mai-500 rounded-full shadow-[0_0_8px_rgba(245,158,11,0.5)]"></span>
                    </button>

                    {showNotifications && (
                        <div className="absolute right-0 top-full mt-2 w-80 bg-dark-900/95 backdrop-blur-xl border border-white/10 rounded-xl shadow-2xl overflow-hidden animate-fade-in ring-1 ring-black/50">
                            <div className="p-4 border-b border-white/5 bg-white/5">
                                <h3 className="text-sm font-semibold text-white">Notificações</h3>
                            </div>
                            <div className="max-h-80 overflow-y-auto custom-scrollbar">
                                <NotificationItem
                                    title="Nova análise disponível"
                                    description="Campanha 'Brand Q1' foi analisada pelo MAI"
                                    time="2 min atrás"
                                    unread
                                />
                                <NotificationItem
                                    title="Alerta de ROAS"
                                    description="ROAS caiu 15% na última semana"
                                    time="1 hora atrás"
                                    unread
                                />
                                <NotificationItem
                                    title="Sincronização concluída"
                                    description="Google Ads sincronizado com sucesso"
                                    time="3 horas atrás"
                                />
                            </div>
                            <div className="p-3 border-t border-white/5 bg-white/5">
                                <button className="w-full py-2 text-sm text-mai-500 hover:text-mai-400 font-medium transition-colors">
                                    Ver todas notificações
                                </button>
                            </div>
                        </div>
                    )}
                </div>

                {/* Profile */}
                <div className="relative">
                    <button
                        onClick={() => setShowProfile(!showProfile)}
                        className="flex items-center gap-3 p-1.5 pr-3 rounded-xl bg-white/5 hover:bg-white/10 transition-colors border border-white/5"
                    >
                        <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-mai-400 to-mai-600 flex items-center justify-center shadow-lg shadow-mai-500/20">
                            <User size={16} className="text-white" />
                        </div>
                        <div className="text-left hidden sm:block">
                            <p className="text-sm font-semibold text-white">Paulo Beber</p>
                            <p className="text-[10px] text-gray-500 uppercase tracking-wider font-bold">Admin</p>
                        </div>
                        <ChevronDown size={16} className="text-gray-500" />
                    </button>

                    {showProfile && (
                        <div className="absolute right-0 top-full mt-2 w-56 bg-dark-900/95 backdrop-blur-xl border border-white/10 rounded-xl shadow-2xl overflow-hidden animate-fade-in ring-1 ring-black/50">
                            <div className="p-4 border-b border-white/5 bg-white/5">
                                <p className="text-sm font-semibold text-white">Paulo Beber</p>
                                <p className="text-xs text-gray-400">paulo@empresa.com</p>
                            </div>
                            <div className="p-2">
                                <ProfileMenuItem label="Meu Perfil" />
                                <ProfileMenuItem label="Configurações" />
                                <ProfileMenuItem label="Suporte" />
                            </div>
                            <div className="p-2 border-t border-white/5">
                                <button className="w-full px-3 py-2 text-sm text-left text-red-400 hover:bg-red-500/10 rounded-lg transition-colors font-medium">
                                    Sair
                                </button>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </header>
    );
}

function NotificationItem({
    title,
    description,
    time,
    unread = false,
}: {
    title: string;
    description: string;
    time: string;
    unread?: boolean;
}) {
    return (
        <div
            className={`p-4 hover:bg-white/5 cursor-pointer transition-colors border-b border-white/5 last:border-0 ${unread ? "bg-mai-500/5" : ""
                }`}
        >
            <div className="flex items-start gap-3">
                {unread && (
                    <span className="mt-1.5 w-2 h-2 bg-mai-500 rounded-full flex-shrink-0 shadow-[0_0_8px_rgba(245,158,11,0.5)]"></span>
                )}
                <div className={unread ? "" : "ml-5"}>
                    <p className={`text-sm font-medium ${unread ? "text-white" : "text-gray-300"}`}>{title}</p>
                    <p className="text-xs text-gray-500 mt-0.5">{description}</p>
                    <p className="text-[10px] text-gray-600 mt-1 font-medium italic">{time}</p>
                </div>
            </div>
        </div>
    );
}

function ProfileMenuItem({ label }: { label: string }) {
    return (
        <button className="w-full px-3 py-2 text-sm text-left text-gray-300 hover:bg-white/5 rounded-lg transition-colors">
            {label}
        </button>
    );
}
