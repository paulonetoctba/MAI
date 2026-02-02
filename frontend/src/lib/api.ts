const API_BASE_URL = 'http://localhost:8000/api/v1';

// Helper to get headers with auth token (Mocked for now since Auth unavailable in Front context)
// In real implementation, this should come from your Auth provider / Context
const getHeaders = () => {
    // TODO: Replace with actual token retrieval
    const token = typeof window !== 'undefined' ? localStorage.getItem('token') : '';
    return {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
    };
};

export const api = {
    get: async <T>(endpoint: string): Promise<T> => {
        const res = await fetch(`${API_BASE_URL}${endpoint}`, {
            headers: getHeaders()
        });
        if (!res.ok) throw new Error('API Request Failed');
        return res.json();
    },

    post: async <T>(endpoint: string, data: any): Promise<T> => {
        const res = await fetch(`${API_BASE_URL}${endpoint}`, {
            method: 'POST',
            headers: getHeaders(),
            body: JSON.stringify(data)
        });
        if (!res.ok) throw new Error('API Request Failed');
        return res.json();
    }
};
