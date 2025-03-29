export type Interaction = {
    id: number;
    prompt: string;
    response: string;
    thumbs: string;
    timestamp: string;      // formato ISO tipo '2025-03-28T14:00:00Z'

    // Campos adicionales opcionales
    score?: number;         // puntuación de evaluación manual (ej. 7.5)
    tags?: string[];        // etiquetas temáticas asignadas
    notes?: string;         // observaciones escritas por el evaluador
    rag_score?: number;     // nivel de confianza o score RAG del modelo
};