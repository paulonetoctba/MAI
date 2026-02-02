export interface Integration {
    id: string;
    key: string;
    name: string;
    category: string;
    logo_url?: string;
    description?: string;
    config_schema: Record<string, any>;
    is_active: boolean;
}

export interface TenantConfig {
    id: string;
    tenant_id: string;
    integration_id: string;
    is_enabled: boolean;
    created_at: string;
    updated_at: string;
}

export interface IntegrationWithConfig extends Integration {
    isEnabled: boolean;
}
