'use client';

import { useState } from 'react';
import { Integration } from '@/types/integration';
import { api } from '@/lib/api';

interface Props {
    integration: Integration;
    onClose: () => void;
    onSuccess: () => void;
}

export default function IntegrationConfigModal({ integration, onClose, onSuccess }: Props) {
    const [formData, setFormData] = useState<Record<string, string>>({});
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            await api.post('/integrations/config', {
                integration_id: integration.id,
                credentials: formData
            });
            onSuccess();
            onClose();
        } catch (err) {
            setError('Failed to save configuration.');
        } finally {
            setLoading(false);
        }
    };

    const handleChange = (key: string, value: string) => {
        setFormData(prev => ({ ...prev, [key]: value }));
    };

    return (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
            <div className="bg-slate-900 border border-slate-700 rounded-lg p-6 max-w-md w-full shadow-xl">
                <h2 className="text-xl font-bold text-white mb-4">
                    Configure {integration.name}
                </h2>

                <form onSubmit={handleSubmit} className="space-y-4">
                    {/* Dynamic Fields based on schema */}
                    {Object.keys(integration.config_schema || {}).map((key) => (
                        <div key={key}>
                            <label className="block text-sm font-medium text-slate-300 mb-1 capitalize">
                                {key.replace(/_/g, ' ')}
                            </label>
                            <input
                                type="text"
                                className="w-full bg-slate-800 border border-slate-600 rounded px-3 py-2 text-white focus:outline-none focus:border-blue-500"
                                value={formData[key] || ''}
                                onChange={(e) => handleChange(key, e.target.value)}
                                required
                            />
                        </div>
                    ))}

                    {error && <p className="text-red-400 text-sm">{error}</p>}

                    <div className="flex justify-end gap-3 mt-6">
                        <button
                            type="button"
                            onClick={onClose}
                            className="px-4 py-2 text-slate-300 hover:text-white"
                        >
                            Cancel
                        </button>
                        <button
                            type="submit"
                            disabled={loading}
                            className="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded disabled:opacity-50"
                        >
                            {loading ? 'Saving...' : 'Connect'}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
}
