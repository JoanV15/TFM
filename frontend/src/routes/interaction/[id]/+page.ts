import type { PageLoad } from './$types';
import { getInteractionById } from '$lib/api/api_frontend';

export const load: PageLoad = async ({ params }) => {
    const interaction = await getInteractionById(params.id);
    return { interaction };
};
