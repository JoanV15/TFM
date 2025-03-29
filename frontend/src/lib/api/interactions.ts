import type { Interaction } from '$lib/types';

const BASE_URL = 'http://localhost:8000'; // Actualízalo si es necesario

// Obtener todas las interacciones con filtros opcionales
export async function getInteractions(filters?: any): Promise<Interaction[]> {
    const res = await fetch(`${BASE_URL}/interactions`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(filters)
    });

    if (!res.ok) {
        throw new Error('Error al obtener las interacciones');
    }

    return await res.json();
}

// Obtener una interacción específica por ID
export async function getInteractionById(id: number): Promise<Interaction> {
    const res = await fetch(`${BASE_URL}/interactions/${id}`);

    if (!res.ok) {
        throw new Error(`Error al obtener la interacción con ID ${id}`);
    }

    return await res.json();
}

// Enviar evaluación a una interacción
export async function postEvaluation(id: number, data: any): Promise<void> {
    const res = await fetch(`${BASE_URL}/evaluation/${id}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });

    if (!res.ok) {
        throw new Error('Error al enviar evaluación');
    }
}
