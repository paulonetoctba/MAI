"use client";

import { useState } from "react";
import {
    Link2,
    CheckCircle,
    XCircle,
    ExternalLink,
    RefreshCw,
    Loader2,
    AlertTriangle,
} from "lucide-react";

interface Integration {
    id: string;
    name: string;
    platform: "google" | "meta" | "tiktok";
    logo: string;
    description: string;
    connected: boolean;
    lastSync?: string;
    accountName?: string;
    accountId?: string;
}

const integrations: Integration[] = [
    {
        id: "google",
        name: "Google Ads",
        platform: "google",
        logo: "/google-ads.svg",
        description: "Conecte sua conta do Google Ads para importar campanhas e métricas",
        connected: false,
    },
    {
        id: "meta",
        name: "Meta Ads",
        platform: "meta",
        logo: "/meta-ads.svg",
        description: "Importe dados do Facebook e Instagram Ads",
        connected: false,
    },
    {
        id: "tiktok",
        name: "TikTok Ads",
        platform: "tiktok",
        logo: "/tiktok-ads.svg",
        description: "Conecte TikTok Business para sincronizar campanhas",
        connected: false,
    },
];

export default function IntegrationsPage() {
    const [integrationsList, setIntegrationsList] = useState(integrations);
    const [syncing, setSyncing] = useState<string | null>(null);
    const [connecting, setConnecting] = useState<string | null>(null);

    const handleConnect = async (id: string) => {
        setConnecting(id);

        // Simulate OAuth flow
        await new Promise((resolve) => setTimeout(resolve, 2000));

        setIntegrationsList((prev) =>
            prev.map((integration) =>
                integration.id === id
                    ? {
                        ...integration,
                        connected: true,
                        accountName: `${integration.name} Demo Account`,
                        accountId: `${id.toUpperCase()}_123456789`,
                        lastSync: "Agora",
                    }
                    : integration
            )
        );

        setConnecting(null);
    };

    const handleDisconnect = (id: string) => {
        setIntegrationsList((prev) =>
            prev.map((integration) =>
                integration.id === id
                    ? {
                        ...integration,
                        connected: false,
                        accountName: undefined,
                        accountId: undefined,
                        lastSync: undefined,
                    }
                    : integration
            )
        );
    };

    const handleSync = async (id: string) => {
        setSyncing(id);
        await new Promise((resolve) => setTimeout(resolve, 3000));

        setIntegrationsList((prev) =>
            prev.map((integration) =>
                integration.id === id
                    ? { ...integration, lastSync: "Agora" }
                    : integration
            )
        );

        setSyncing(null);
    };

    return (
        <div className="max-w-4xl mx-auto space-y-6">
            {/* Page Header */}
            <div>
                <h1 className="text-2xl font-bold text-white">Integrações de Canais</h1>
                <p className="text-gray-500">
                    Conecte suas plataformas de ads para sincronizar dados automaticamente
                </p>
            </div>

            {/* Info Banner */}
            <div className="p-4 rounded-xl bg-mai-500/10 border border-mai-500/20 flex items-start gap-3">
                <AlertTriangle size={20} className="text-mai-400 flex-shrink-0 mt-0.5" />
                <div>
                    <p className="text-sm text-white font-medium">Configuração Necessária</p>
                    <p className="text-xs text-gray-400 mt-1">
                        Para conectar as plataformas, você precisa configurar as credenciais OAuth no arquivo
                        <code className="mx-1 px-1.5 py-0.5 bg-white/10 rounded">.env</code>
                        do backend. Consulte a documentação para mais detalhes.
                    </p>
                </div>
            </div>

            {/* Integrations List */}
            <div className="space-y-4">
                {integrationsList.map((integration) => (
                    <IntegrationCard
                        key={integration.id}
                        integration={integration}
                        onConnect={() => handleConnect(integration.id)}
                        onDisconnect={() => handleDisconnect(integration.id)}
                        onSync={() => handleSync(integration.id)}
                        isConnecting={connecting === integration.id}
                        isSyncing={syncing === integration.id}
                    />
                ))}
            </div>

            {/* Sync Status */}
            <div className="p-6 rounded-2xl bg-dark-900 border border-white/5">
                <h3 className="text-lg font-semibold text-white mb-4">Status de Sincronização</h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <StatusCard
                        label="Campanhas Sincronizadas"
                        value="0"
                        description="Nenhuma campanha"
                    />
                    <StatusCard
                        label="Última Sincronização"
                        value="—"
                        description="Nenhuma sincronização"
                    />
                    <StatusCard
                        label="Contas Conectadas"
                        value={integrationsList.filter((i) => i.connected).length.toString()}
                        description={`de ${integrationsList.length} disponíveis`}
                    />
                </div>
            </div>
        </div>
    );
}

function IntegrationCard({
    integration,
    onConnect,
    onDisconnect,
    onSync,
    isConnecting,
    isSyncing,
}: {
    integration: Integration;
    onConnect: () => void;
    onDisconnect: () => void;
    onSync: () => void;
    isConnecting: boolean;
    isSyncing: boolean;
}) {
    const platformColors = {
        google: "from-blue-500/20 to-red-500/20",
        meta: "from-blue-600/20 to-purple-600/20",
        tiktok: "from-pink-500/20 to-cyan-500/20",
    };

    const platformIcons = {
        google: "🔍",
        meta: "📘",
        tiktok: "🎵",
    };

    return (
        <div className="p-6 rounded-2xl bg-dark-900 border border-white/5 hover:border-white/10 transition-all">
            <div className="flex items-start justify-between">
                <div className="flex items-start gap-4">
                    {/* Platform Icon */}
                    <div
                        className={`w-14 h-14 rounded-xl bg-gradient-to-br ${platformColors[integration.platform]
                            } flex items-center justify-center text-2xl`}
                    >
                        {platformIcons[integration.platform]}
                    </div>

                    {/* Info */}
                    <div>
                        <div className="flex items-center gap-2">
                            <h3 className="text-lg font-semibold text-white">{integration.name}</h3>
                            {integration.connected ? (
                                <span className="flex items-center gap-1 px-2 py-0.5 bg-green-500/10 text-green-400 rounded text-xs">
                                    <CheckCircle size={12} />
                                    Conectado
                                </span>
                            ) : (
                                <span className="flex items-center gap-1 px-2 py-0.5 bg-gray-500/10 text-gray-400 rounded text-xs">
                                    <XCircle size={12} />
                                    Desconectado
                                </span>
                            )}
                        </div>
                        <p className="text-sm text-gray-500 mt-1">{integration.description}</p>

                        {integration.connected && (
                            <div className="mt-3 space-y-1">
                                <p className="text-xs text-gray-400">
                                    <span className="text-gray-500">Conta:</span> {integration.accountName}
                                </p>
                                <p className="text-xs text-gray-400">
                                    <span className="text-gray-500">ID:</span> {integration.accountId}
                                </p>
                                <p className="text-xs text-gray-400">
                                    <span className="text-gray-500">Última sincronização:</span>{" "}
                                    {integration.lastSync}
                                </p>
                            </div>
                        )}
                    </div>
                </div>

                {/* Actions */}
                <div className="flex flex-col gap-2">
                    {integration.connected ? (
                        <>
                            <button
                                onClick={onSync}
                                disabled={isSyncing}
                                className="flex items-center gap-2 px-4 py-2 bg-mai-500 hover:bg-mai-400 disabled:bg-mai-500/50 text-white rounded-lg text-sm font-medium transition-colors"
                            >
                                {isSyncing ? (
                                    <>
                                        <Loader2 size={14} className="animate-spin" />
                                        Sincronizando...
                                    </>
                                ) : (
                                    <>
                                        <RefreshCw size={14} />
                                        Sincronizar
                                    </>
                                )}
                            </button>
                            <button
                                onClick={onDisconnect}
                                className="flex items-center gap-2 px-4 py-2 border border-red-500/30 text-red-400 hover:bg-red-500/10 rounded-lg text-sm font-medium transition-colors"
                            >
                                <XCircle size={14} />
                                Desconectar
                            </button>
                        </>
                    ) : (
                        <button
                            onClick={onConnect}
                            disabled={isConnecting}
                            className="flex items-center gap-2 px-4 py-2 bg-mai-500 hover:bg-mai-400 disabled:bg-mai-500/50 text-white rounded-lg text-sm font-medium transition-colors"
                        >
                            {isConnecting ? (
                                <>
                                    <Loader2 size={14} className="animate-spin" />
                                    Conectando...
                                </>
                            ) : (
                                <>
                                    <Link2 size={14} />
                                    Conectar
                                </>
                            )}
                        </button>
                    )}
                </div>
            </div>
        </div>
    );
}

function StatusCard({
    label,
    value,
    description,
}: {
    label: string;
    value: string;
    description: string;
}) {
    return (
        <div className="p-4 rounded-xl bg-white/5">
            <p className="text-xs text-gray-500 mb-1">{label}</p>
            <p className="text-2xl font-bold text-white">{value}</p>
            <p className="text-xs text-gray-600 mt-1">{description}</p>
        </div>
    );
}
