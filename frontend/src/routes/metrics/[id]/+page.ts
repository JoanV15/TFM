import type { PageLoad } from './$types';
import { getInteractionById } from '$lib/api/api_frontend';

export const load: PageLoad = async ({ params }) => {
    const id = params.id;
    const interaction = await getInteractionById(id);

    return {
        interaction
    };
};
