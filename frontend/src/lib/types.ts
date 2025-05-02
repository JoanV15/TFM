export type Interaction = {
    id: string;
    parent_id?: string | null;

    prompt: string;
    response: string;

    model?: string;
    timestamp: string;

    rating?: number; // -1, 0, 1 (thumbs)
    score?: number;  // 0–10 manual
    notes?: string;
    tags?: string[];
    chat_title?: string;
    feedback_id?: string | null;
    usage?: Record<string, any>;
    chat_id?: string;

    hallucination?: number;
    moderation?: number;
    context_precision?: number;
    context_recall?: number;
    usefulness?: number;
    answer_relevance?: number;
    g_eval?: number;
};
