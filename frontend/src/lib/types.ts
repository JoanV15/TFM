export type Interaction = {
    id: number;
    parent_id?: number | null;

    role: 'user' | 'assistant';
    content: string;

    model?: string;
    timestamp: string; // ISO format: '2025-03-28T14:00:00Z'

    rating?: number; // Evaluación numérica (0-10, por ejemplo)
    tags?: string[];
    feedback_id?: string | null;

    // Campos adicionales opcionales
    score?: number;     // Puntuación manual alternativa (ej. para pruebas internas)
    notes?: string;     // Observaciones del evaluador
    rag_score?: number; // Score de relevancia/confianza tipo RAG

    // Campo virtual (por compatibilidad con versiones anteriores)
    prompt?: string;    // Si quieres mantenerlo para evitar errores en componentes antiguos
    response?: string;  // Puede mapearse localmente desde `role === 'assistant'`
    thumbs?: string;    // 'up' | 'down' si lo usas como alternativa a `rating`
};
