<script lang="ts">
	import InteractionDetail from '$lib/components/InteractionDetail.svelte';
	import { getInteractionById } from '$lib/api/interactions';
	import type { Interaction } from '$lib/types';
	import type { LoadEvent } from '@sveltejs/kit';
	import { goto } from '$app/navigation';

	export let data: {
		interaction: Interaction;
	};

	// Esta función la ejecuta el router de SvelteKit al cargar esta ruta
	export const load = async ({ params }: LoadEvent) => {
		if (!params.id) {
			throw new Error('ID no proporcionado en la URL');
		}

		const id = parseInt(params.id);
		const interaction = await getInteractionById(id);

		return {
			interaction
		};
	};
</script>

<section class="mx-auto max-w-4xl p-6">
	<h1 class="mb-4 text-2xl font-bold">Detalle de la interacción #{data.interaction.id}</h1>
	<InteractionDetail interaction={data.interaction} />
	<button on:click={() => goto('/')} class="mb-4 text-sm text-blue-600 hover:underline">
		← Volver al listado
	</button>
</section>
