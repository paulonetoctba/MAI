"use client";

import { useState } from "react";
import { Search, Bell, User, ChevronDown } from "lucide-react";

export function Header() {
    const [showNotifications, setShowNotifications] = useState(false);
    const [showProfile, setShowProfile] = useState(false);

    return (
        <header className="h-20 bg-white border-b border-stroke flex items-center justify-between px-6 sticky top-0 z-30 shadow-default">
            {/* Search */}
            <div className="relative w-96">
                <Search
                    size={18}
                    className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400"
                />
                <input
                    type="text"
                    placeholder="Buscar decisões, campanhas..."
                    className="w-full pl-12 pr-4 py-2.5 bg-gray-100 border border-gray-200 rounded-xl text-sm text-black placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-mai-500/20 transition-all font-medium"
                />
                <kbd className="absolute right-4 top-1/2 -translate-y-1/2 px-2 py-0.5 bg-white rounded text-[10px] text-gray-400 border border-gray-200">
                    ⌘K
                </kbd>
            </div>

            {/* Right Side */}
            <div className="flex items-center gap-4">
                {/* Notifications */}
                <div className="relative">
                    <button
                        onClick={() => setShowNotifications(!showNotifications)}
                        className="relative p-2.5 rounded-xl bg-gray-100 hover:bg-gray-200 text-gray-600 transition-colors border border-gray-200"
                    >
                        <Bell size={18} />
                        <span className="absolute top-1.5 right-1.5 w-2.5 h-2.5 bg-red-500 rounded-full border-2 border-white"></span>
                    </button>

                    {showNotifications && (
                        <div className="absolute right-0 top-full mt-2 w-80 bg-white border border-gray-200 rounded-xl shadow-default overflow-hidden animate-fade-in ring-1 ring-black/5">
                            <div className="p-4 border-b border-gray-100 bg-gray-50/50">
                                <h3 className="text-sm font-semibold text-black">Notificações</h3>
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
                            <div className="p-3 border-t border-gray-100 bg-gray-50/50">
                                <button className="w-full py-2 text-sm text-mai-500 hover:text-mai-600 font-medium transition-colors">
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
                        className="flex items-center gap-3 p-1.5 pr-3 rounded-xl bg-gray-100 hover:bg-gray-200 transition-colors border border-gray-200"
                    >
                        <div className="w-8 h-8 rounded-lg bg-mai-500 flex items-center justify-center shadow-sm">
                            <User size={16} className="text-white" />
                        </div>
                        <div className="text-left hidden sm:block">
                            <p className="text-sm font-semibold text-black">Paulo Beber</p>
                            <p className="text-[10px] text-gray-500 font-medium">Administrador</p>
                        </div>
                        <ChevronDown size={14} className="text-gray-400" />
                    </button>

                    {showProfile && (
                        <div className="absolute right-0 top-full mt-2 w-56 bg-white border border-gray-200 rounded-xl shadow-default overflow-hidden animate-fade-in ring-1 ring-black/5">
                            <div className="p-4 border-b border-gray-100 bg-gray-50/50">
                                <p className="text-sm font-semibold text-black">Paulo Beber</p>
                                <p className="text-xs text-gray-500">paulo@empresa.com</p>
                            </div>
                            <div className="p-2">
                                <ProfileMenuItem label="Meu Perfil" />
                                <ProfileMenuItem label="Configurações" />
                                <ProfileMenuItem label="Suporte" />
                            </div>
                            <div className="p-2 border-t border-gray-100">
                                <button className="w-full px-3 py-2 text-sm text-left text-red-500 hover:bg-red-50 rounded-lg transition-colors font-medium text-center">
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
