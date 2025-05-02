import type { Interaction } from '$lib/types';
import { PUBLIC_BACKEND_URL } from '$lib/config';

export type InteractionFilters = {
    limit?: number;
    offset?: number;
    rating?: number;
    score?: number | 'null';
    model?: string;
    tag?: string;
    date_from?: string;
    date_to?: string;
    search?: string;
};

export async function getInteractions(filters: InteractionFilters = {}): Promise<Interaction[]> {
    const params = new URLSearchParams();

    if (filters.limit) params.append('limit', filters.limit.toString());
    if (filters.offset) params.append('offset', filters.offset.toString());
    if (filters.rating !== undefined) params.append('rating', filters.rating.toString());
    if (filters.score !== undefined) params.append('score', filters.score.toString());
    if (filters.model) params.append('model', filters.model);
    if (filters.tag) params.append('tag', filters.tag);
    if (filters.date_from) params.append('date_from', filters.date_from);
    if (filters.date_to) params.append('date_to', filters.date_to);
    if (filters.search) params.append('search', filters.search);

    const url = `${PUBLIC_BACKEND_URL}/interactions?${params.toString()}`;
    const res = await fetch(url);

    if (!res.ok) {
        throw new Error(`Error al obtener las interacciones: ${res.status}`);
    }

    return await res.json();
}

export async function getInteractionById(id: string): Promise<Interaction> {
    const res = await fetch(`${PUBLIC_BACKEND_URL}/interactions/${id}`);

    if (!res.ok) {
        throw new Error(`Error al obtener la interacción con ID ${id}`);
    }

    return await res.json();
}

export async function postEvaluation(id: string, data: {
    rating?: number;
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

export type ExportResult = {
    evaluated_ids: string[];
    skipped_count: number;
    file: string;
};

export async function exportInteractions(): Promise<ExportResult> {
    const res = await fetch(`${PUBLIC_BACKEND_URL}/export_interactions?ts=${Date.now()}`);
    if (!res.ok) {
        throw new Error('Error al exportar interacciones');
    }
    return await res.json();
}

export type StatsResponse = {
    total_interactions: number;
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

export type HeuristicMetricsRequest = {
    expected_output: string;
    actual_output: string;
};

export type HeuristicMetricsResponse = {
    equals: boolean;
    contains: boolean;
    regexmatch: boolean;
    isjson: boolean;
    levenshtein: number;
};

export async function getHeuristicMetrics(data: HeuristicMetricsRequest): Promise<HeuristicMetricsResponse> {
    const res = await fetch(`${PUBLIC_BACKEND_URL}/metrics/heuristics`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });

    if (!res.ok) {
        throw new Error('Error al calcular métricas heurísticas');
    }

    return await res.json();
}

export async function evaluateWithOpik(id: string): Promise<void> {
    const res = await fetch(`${PUBLIC_BACKEND_URL}/opik/evaluate/${id}`, {
        method: 'POST'
    });
    if (!res.ok) {
        throw new Error('Error al evaluar con Opik');
    }
}

// 🔄 Sincronización con WebUI
export async function syncWebuiDB(): Promise<void> {
    const res = await fetch(`${PUBLIC_BACKEND_URL}/sync_webui_db`, {
        method: 'POST'
    });
    if (!res.ok) {
        throw new Error('Error al sincronizar con webui.db');
    }
}
