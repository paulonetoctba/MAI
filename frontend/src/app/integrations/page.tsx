'use client';

import { useEffect, useState } from 'react';
import { api } from '@/lib/api';
import { Integration, TenantConfig, IntegrationWithConfig } from '@/types/integration';
import IntegrationCard from '@/components/IntegrationCard';
import IntegrationConfigModal from '@/components/IntegrationConfigModal';
import { LayoutGrid, ShoppingCart, Megaphone, Wrench } from 'lucide-react';

export default function IntegrationsPage() {
    const [integrations, setIntegrations] = useState<IntegrationWithConfig[]>([]);
    const [loading, setLoading] = useState(true);
    const [selectedCategory, setSelectedCategory] = useState<string>('all');
    const [setupIntegration, setSetupIntegration] = useState<Integration | null>(null);

    const categories = [
        { id: 'all', label: 'All Apps', icon: LayoutGrid },
        { id: 'ecommerce', label: 'Ecommerce', icon: ShoppingCart },
        { id: 'ads', label: 'Ads & Social', icon: Megaphone },
        { id: 'tools', label: 'Tools', icon: Wrench },
    ];

    const fetchIntegrations = async () => {
        try {
            setLoading(true);
            const [allIntegrations, userConfigs] = await Promise.all([
                api.get<Integration[]>('/integrations/'),
                api.get<TenantConfig[]>('/integrations/config')
            ]);

            const configMap = new Set(userConfigs.map(c => c.integration_id));

            const merged = allIntegrations.map(i => ({
                ...i,
                isEnabled: configMap.has(i.id)
            }));

            setIntegrations(merged);
        } catch (error) {
            console.error('Failed to load integrations', error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchIntegrations();
    }, []);

    const filteredIntegrations = selectedCategory === 'all'
        ? integrations
        : integrations.filter(i => i.category.toLowerCase().includes(selectedCategory));

    return (
        <div className="p-8 max-w-7xl mx-auto">
            <div className="mb-8">
                <h1 className="text-3xl font-bold text-white mb-2">Integrations Marketplace</h1>
                <p className="text-slate-400">Connect your tools to power up your marketing intelligence.</p>
            </div>

            {/* Categories */}
            <div className="flex gap-4 mb-8 overflow-x-auto pb-2">
                {categories.map(cat => (
                    <button
                        key={cat.id}
                        onClick={() => setSelectedCategory(cat.id)}
                        className={`flex items-center gap-2 px-4 py-2 rounded-full text-sm font-medium transition-colors whitespace-nowrap ${selectedCategory === cat.id
                                ? 'bg-blue-600 text-white'
                                : 'bg-slate-800 text-slate-300 hover:bg-slate-700'
                            }`}
                    >
                        <cat.icon size={16} />
                        {cat.label}
                    </button>
                ))}
            </div>

            {/* Grid */}
            {loading ? (
                <div className="text-center py-20 text-slate-500">Loading integrations...</div>
            ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                    {filteredIntegrations.map(integration => (
                        <IntegrationCard
                            key={integration.id}
                            integration={integration}
                            onConfigure={(i) => setSetupIntegration(i)}
                        />
                    ))}
                </div>
            )}

            {/* Modal */}
            {setupIntegration && (
                <IntegrationConfigModal
                    integration={setupIntegration}
                    onClose={() => setSetupIntegration(null)}
                    onSuccess={() => {
                        fetchIntegrations(); // Refresh state
                    }}
                />
            )}
        </div>
    );
}
