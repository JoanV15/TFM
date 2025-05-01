import type { Interaction } from '$lib/types';
import { PUBLIC_BACKEND_URL } from '$lib/config';

export type InteractionFilters = {
    limit?: number;
    offset?: number;
    role?: string;
    rating?: number;
    model?: string;
    tags?: string;
};

// GET /interactions con filtros y paginación
export async function getInteractions(filters: InteractionFilters = {}): Promise<Interaction[]> {
    const params = new URLSearchParams();

    if (filters.limit) params.append('limit', filters.limit.toString());
    if (filters.offset) params.append('offset', filters.offset.toString());
    if (filters.role) params.append('role', filters.role);
    if (filters.rating !== undefined) params.append('rating', filters.rating.toString());
    if (filters.model) params.append('model', filters.model);
    if (filters.tags) params.append('tags', filters.tags);
    if ((filters as any).date_from) params.append('date_from', (filters as any).date_from);
    if ((filters as any).date_to) params.append('date_to', (filters as any).date_to);
    if ((filters as any).search) params.append('search', (filters as any).search);

    const url = `${PUBLIC_BACKEND_URL}/interactions?${params.toString()}`;
    console.log("🌐 GET /interactions →", url);

    const res = await fetch(url);

    if (!res.ok) {
        const text = await res.text();
        console.error("❌ Error HTTP:", res.status, text);
        throw new Error(`Error al obtener las interacciones: ${res.status}`);
    }

    try {
        const json = await res.json();
        console.log("📦 JSON recibido:", json);
        return json;
    } catch (err) {
        console.error("❌ Error al parsear JSON:", err);
        throw new Error("Error al interpretar la respuesta del servidor");
    }
}


// GET /interactions/{id}
export async function getInteractionById(id: number): Promise<Interaction> {
    const res = await fetch(`${PUBLIC_BACKEND_URL}/interactions/${id}`);

    if (!res.ok) {
        throw new Error(`Error al obtener la interacción con ID ${id}`);
    }

    return await res.json();
}

// POST /evaluation/{id}
export async function postEvaluation(id: number, data: {
    score?: number;
    notes?: string;
    tags?: string[];
}): Promise<void> {
    const res = await fetch(`${PUBLIC_BACKEND_URL}/evaluation/${id}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });

    if (!res.ok) {
        throw new Error('Error al enviar evaluación');
    }
}

// GET /stats
export type StatsResponse = {
    total_interactions: number;
    total_user_messages: number;
    total_assistant_messages: number;
    rated_positive: number;
    rated_negative: number;
    rated_neutral: number;
    models_usage: Record<string, number>;
    tags_usage: Record<string, number>;
};

export async function getStats(): Promise<StatsResponse> {
    const res = await fetch(`${PUBLIC_BACKEND_URL}/stats`);
    if (!res.ok) {
        throw new Error('Error al obtener estadísticas');
    }
    return await res.json();
}
