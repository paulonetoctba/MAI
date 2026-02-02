"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
    LayoutDashboard,
    Search,
    Share2,
    Video,
    ShoppingCart,
    MonitorPlay,
    Mail,
    Settings,
    ChevronLeft,
    ChevronRight,
    LogOut,
    ChevronDown,
    ChevronUp,
    BarChart3,
    Brain,
} from "lucide-react";
import { LogoFull } from "@/components/ui/Logo";
import { cn } from "@/lib/utils";

interface SubItem {
    label: string;
    href: string;
}

interface MenuCategory {
    label: string;
    icon: React.ElementType;
    items: SubItem[];
}

const MENU_CATEGORIES: MenuCategory[] = [
    {
        label: "Search & Performance",
        icon: Search,
        items: [
            { label: "Google Ads", href: "/dashboard/integrations/google-ads" },
            { label: "Google Analytics 4", href: "/dashboard/integrations/ga4" },
            { label: "Search Console", href: "/dashboard/integrations/search-console" },
            { label: "YouTube Ads", href: "/dashboard/integrations/youtube-ads" },
            { label: "Bing Ads", href: "/dashboard/integrations/bing-ads" },
        ],
    },
    {
        label: "Social Media & Ads",
        icon: Share2,
        items: [
            { label: "Meta (FB & IG)", href: "/dashboard/integrations/meta" },
            { label: "LinkedIn Marketing", href: "/dashboard/integrations/linkedin" },
            { label: "TikTok Marketing", href: "/dashboard/integrations/tiktok" },
            { label: "X (Twitter) Ads", href: "/dashboard/integrations/x-ads" },
            { label: "Pinterest Ads", href: "/dashboard/integrations/pinterest" },
            { label: "Reddit Ads", href: "/dashboard/integrations/reddit" },
        ],
    },
    {
        label: "Vídeo & Creators",
        icon: Video,
        items: [
            { label: "YouTube Data", href: "/dashboard/integrations/youtube-data" },
            { label: "Twitch", href: "/dashboard/integrations/twitch" },
            { label: "TikTok Creator", href: "/dashboard/integrations/tiktok-creator" },
            { label: "Meta Creator", href: "/dashboard/integrations/meta-creator" },
        ],
    },
    {
        label: "Retail Media",
        icon: ShoppingCart,
        items: [
            { label: "Amazon Ads", href: "/dashboard/integrations/amazon-ads" },
            { label: "Mercado Livre Ads", href: "/dashboard/integrations/mercadolivre-ads" },
            { label: "Shopee Ads", href: "/dashboard/integrations/shopee-ads" },
            { label: "Magalu Ads", href: "/dashboard/integrations/magalu-ads" },
            { label: "Walmart Connect", href: "/dashboard/integrations/walmart" },
            { label: "AliExpress Ads", href: "/dashboard/integrations/aliexpress" },
        ],
    },
    {
        label: "Programmatic",
        icon: MonitorPlay,
        items: [
            { label: "DV360", href: "/dashboard/integrations/dv360" },
            { label: "The Trade Desk", href: "/dashboard/integrations/ttd" },
            { label: "Amazon DSP", href: "/dashboard/integrations/amazon-dsp" },
            { label: "Criteo", href: "/dashboard/integrations/criteo" },
            { label: "Adform", href: "/dashboard/integrations/adform" },
        ],
    },
    {
        label: "Owned Media & CRM",
        icon: Mail,
        items: [
            { label: "HubSpot", href: "/dashboard/integrations/hubspot" },
            { label: "Salesforce MC", href: "/dashboard/integrations/salesforce" },
            { label: "RD Station", href: "/dashboard/integrations/rdstation" },
            { label: "Mailchimp", href: "/dashboard/integrations/mailchimp" },
            { label: "ActiveCampaign", href: "/dashboard/integrations/activecampaign" },
            { label: "WhatsApp Cloud", href: "/dashboard/integrations/whatsapp" },
            { label: "Twilio", href: "/dashboard/integrations/twilio" },
            { label: "SendGrid", href: "/dashboard/integrations/sendgrid" },
            { label: "Firebase Cloud", href: "/dashboard/integrations/firebase" },
        ],
    },
];

export function Sidebar() {
    const [collapsed, setCollapsed] = useState(false);
    const [expandedCategory, setExpandedCategory] = useState<string | null>(null);
    const pathname = usePathname();

    const toggleCategory = (label: string) => {
        if (collapsed) {
            setCollapsed(false);
            setExpandedCategory(label);
        } else {
            setExpandedCategory(expandedCategory === label ? null : label);
        }
    };

    return (
        <aside
            className={cn(
                "fixed left-0 top-0 z-40 h-screen bg-dark-900 border-r border-white/5 transition-all duration-300 flex flex-col",
                collapsed ? "w-16" : "w-72"
            )}
        >
            {/* Logo */}
            <div className="h-16 flex items-center justify-between px-4 border-b border-white/5 bg-dark-950/50 backdrop-blur-md">
                {!collapsed && <LogoFull />}
                {collapsed && (
                    <div className="w-8 h-8 rounded-lg bg-mai-500 flex items-center justify-center mx-auto">
                        <span className="text-white font-bold text-sm">M</span>
                    </div>
                )}
                <button
                    onClick={() => setCollapsed(!collapsed)}
                    className="p-1.5 rounded-lg hover:bg-white/5 text-gray-400 hover:text-mai-400 transition-colors"
                >
                    {collapsed ? <ChevronRight size={18} /> : <ChevronLeft size={18} />}
                </button>
            </div>

            {/* Main Navigation */}
            <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto custom-scrollbar">
                {/* Dashboard Link */}
                <Link
                    href="/dashboard"
                    className={cn(
                        "flex items-center gap-3 px-3 py-2.5 rounded-xl transition-all duration-200 mb-4",
                        pathname === "/dashboard"
                            ? "bg-mai-500/10 text-mai-400 border border-mai-500/20"
                            : "text-gray-400 hover:text-white hover:bg-white/5"
                    )}
                >
                    <LayoutDashboard size={20} />
                    {!collapsed && <span className="text-sm font-medium">Dashboard</span>}
                </Link>

                <div className="text-[10px] font-bold text-gray-500 uppercase tracking-widest px-3 mb-2">
                    {!collapsed ? "Integrações" : "•••"}
                </div>

                {MENU_CATEGORIES.map((cat) => {
                    const isExpanded = expandedCategory === cat.label;
                    const hasActiveChild = cat.items.some(item => pathname === item.href);

                    return (
                        <div key={cat.label} className="space-y-1">
                            <button
                                onClick={() => toggleCategory(cat.label)}
                                className={cn(
                                    "w-full flex items-center justify-between px-3 py-2.5 rounded-xl transition-all duration-200",
                                    hasActiveChild
                                        ? "text-mai-400 bg-mai-500/5 shadow-sm"
                                        : "text-gray-400 hover:text-white hover:bg-white/5"
                                )}
                            >
                                <div className="flex items-center gap-3">
                                    <cat.icon size={20} className={hasActiveChild ? "text-mai-400" : ""} />
                                    {!collapsed && (
                                        <span className="text-sm font-medium truncate max-w-[160px]">
                                            {cat.label}
                                        </span>
                                    )}
                                </div>
                                {!collapsed && (
                                    isExpanded ? <ChevronUp size={14} /> : <ChevronDown size={14} />
                                )}
                            </button>

                            {isExpanded && !collapsed && (
                                <div className="ml-9 space-y-1 animate-fade-in border-l border-white/5 pl-2">
                                    {cat.items.map((item) => (
                                        <Link
                                            key={item.href}
                                            href={item.href}
                                            className={cn(
                                                "block px-3 py-1.5 text-xs rounded-lg transition-colors",
                                                pathname === item.href
                                                    ? "text-mai-400 font-medium"
                                                    : "text-gray-500 hover:text-white"
                                            )}
                                        >
                                            {item.label}
                                        </Link>
                                    ))}
                                </div>
                            )}
                        </div>
                    );
                })}
            </nav>

            {/* Bottom Section */}
            <div className="px-3 py-4 border-t border-white/5 bg-dark-950/30">
                <Link
                    href="/dashboard/settings"
                    className={cn(
                        "flex items-center gap-3 px-3 py-2.5 rounded-xl transition-all duration-200 text-gray-400 hover:text-white hover:bg-white/5"
                    )}
                >
                    <Settings size={20} />
                    {!collapsed && <span className="text-sm font-medium">Configurações</span>}
                </Link>

                <button
                    className="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-gray-400 hover:text-red-400 hover:bg-red-500/5 transition-all duration-200 mt-1"
                >
                    <LogOut size={20} />
                    {!collapsed && <span className="text-sm font-medium">Sair</span>}
                </button>
            </div>
        </aside>
    );
}
