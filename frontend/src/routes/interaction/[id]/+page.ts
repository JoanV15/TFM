// /routes/interaction/[id]/+page.ts
import { getInteractionById } from '$lib/api/interactions';
import type { Load } from '@sveltejs/kit';

export const load: Load = async ({ params }) => {
    if (!params.id) {
        throw new Error('ID no proporcionado');
    }

    const id = parseInt(params.id);
    const interaction = await getInteractionById(id);

    return { interaction };
};
