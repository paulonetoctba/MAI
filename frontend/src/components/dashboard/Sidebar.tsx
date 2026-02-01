"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
    LayoutDashboard,
    Brain,
    BarChart3,
    Settings,
    ChevronLeft,
    ChevronRight,
    Zap,
    LogOut,
    Link2,
} from "lucide-react";
import { Logo } from "@/components/ui/Logo";
import { cn } from "@/lib/utils";

interface NavItem {
    label: string;
    href: string;
    icon: React.ElementType;
}

const mainNavItems: NavItem[] = [
    { label: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
    { label: "Decisões", href: "/dashboard/decisions", icon: Brain },
    { label: "Campanhas", href: "/dashboard/campaigns", icon: BarChart3 },
];

const bottomNavItems: NavItem[] = [
    { label: "Integrações", href: "/dashboard/settings/integrations", icon: Link2 },
    { label: "Configurações", href: "/dashboard/settings", icon: Settings },
];

export function Sidebar() {
    const [collapsed, setCollapsed] = useState(false);
    const pathname = usePathname();

    return (
        <aside
            className={cn(
                "fixed left-0 top-0 z-40 h-screen bg-dark-900 border-r border-white/5 transition-all duration-300 flex flex-col",
                collapsed ? "w-16" : "w-64"
            )}
        >
            {/* Logo */}
            <div className="h-16 flex items-center justify-between px-4 border-b border-white/5">
                {!collapsed && <Logo variant="full" />}
                {collapsed && <Logo variant="icon" />}
                <button
                    onClick={() => setCollapsed(!collapsed)}
                    className="p-1.5 rounded-lg hover:bg-white/5 text-gray-400 hover:text-white transition-colors"
                >
                    {collapsed ? <ChevronRight size={18} /> : <ChevronLeft size={18} />}
                </button>
            </div>

            {/* Main Navigation */}
            <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
                {mainNavItems.map((item) => {
                    const isActive = pathname === item.href;
                    return (
                        <Link
                            key={item.href}
                            href={item.href}
                            className={cn(
                                "flex items-center gap-3 px-3 py-2.5 rounded-xl transition-all duration-200",
                                isActive
                                    ? "bg-mai-500/10 text-mai-400 border border-mai-500/20"
                                    : "text-gray-400 hover:text-white hover:bg-white/5"
                            )}
                        >
                            <item.icon size={20} className={isActive ? "text-mai-400" : ""} />
                            {!collapsed && (
                                <span className="text-sm font-medium">{item.label}</span>
                            )}
                        </Link>
                    );
                })}
            </nav>

            {/* Bottom Navigation */}
            <div className="px-3 py-4 border-t border-white/5 space-y-1">
                {bottomNavItems.map((item) => {
                    const isActive = pathname === item.href || pathname.startsWith(item.href + "/");
                    return (
                        <Link
                            key={item.href}
                            href={item.href}
                            className={cn(
                                "flex items-center gap-3 px-3 py-2.5 rounded-xl transition-all duration-200",
                                isActive
                                    ? "bg-mai-500/10 text-mai-400 border border-mai-500/20"
                                    : "text-gray-400 hover:text-white hover:bg-white/5"
                            )}
                        >
                            <item.icon size={20} className={isActive ? "text-mai-400" : ""} />
                            {!collapsed && (
                                <span className="text-sm font-medium">{item.label}</span>
                            )}
                        </Link>
                    );
                })}

                {/* Logout */}
                <button
                    className="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-gray-400 hover:text-red-400 hover:bg-red-500/5 transition-all duration-200"
                >
                    <LogOut size={20} />
                    {!collapsed && <span className="text-sm font-medium">Sair</span>}
                </button>
            </div>

            {/* Upgrade Banner */}
            {!collapsed && (
                <div className="mx-3 mb-4 p-4 rounded-xl bg-gradient-to-br from-mai-600/20 to-purple-600/20 border border-mai-500/20">
                    <div className="flex items-center gap-2 mb-2">
                        <Zap size={16} className="text-mai-400" />
                        <span className="text-sm font-semibold text-white">MAI Pro</span>
                    </div>
                    <p className="text-xs text-gray-400 mb-3">
                        Desbloqueie análises ilimitadas e integrações avançadas.
                    </p>
                    <button className="w-full py-2 px-3 text-xs font-semibold rounded-lg bg-mai-500 hover:bg-mai-400 text-white transition-colors">
                        Fazer Upgrade
                    </button>
                </div>
            )}
        </aside>
    );
}
