'use client';

import { IntegrationWithConfig } from '@/types/integration';
// Using Lucide Icons if available, else simple svg
import { Link, CheckCircle, PlusCircle } from 'lucide-react';

interface Props {
    integration: IntegrationWithConfig;
    onConfigure: (integration: IntegrationWithConfig) => void;
}

export default function IntegrationCard({ integration, onConfigure }: Props) {
    return (
        <div className="bg-slate-800 border border-slate-700 rounded-lg p-5 flex flex-col hover:border-slate-500 transition-colors">
            <div className="flex items-start justify-between mb-4">
                <div className="w-12 h-12 bg-slate-700 rounded-full flex items-center justify-center text-xl font-bold text-slate-300">
                    {integration.logo_url ? (
                        <img src={integration.logo_url} alt={integration.name} className="w-8 h-8 object-contain" />
                    ) : (
                        integration.name.substring(0, 2).toUpperCase()
                    )}
                </div>
                {integration.isEnabled && (
                    <div className="text-green-400 flex items-center gap-1 text-xs font-semibold bg-green-400/10 px-2 py-1 rounded-full">
                        <CheckCircle size={12} />
                        Active
                    </div>
                )}
            </div>

            <h3 className="text-lg font-semibold text-white mb-1">{integration.name}</h3>
            <p className="text-sm text-slate-400 mb-4 flex-grow line-clamp-2">
                {integration.description || `Integrate with ${integration.name}`}
            </p>

            <button
                onClick={() => onConfigure(integration)}
                className={`w-full py-2 px-3 rounded flex items-center justify-center gap-2 text-sm font-medium transition-colors ${integration.isEnabled
                        ? 'bg-slate-700 text-slate-200 hover:bg-slate-600'
                        : 'bg-blue-600 text-white hover:bg-blue-500'
                    }`}
            >
                {integration.isEnabled ? 'Configure' : 'Connect'}
            </button>
        </div>
    );
}
