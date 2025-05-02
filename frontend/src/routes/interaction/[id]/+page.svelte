<script lang="ts">
	import InteractionDetail from '$lib/components/InteractionDetail.svelte';
	import type { Interaction } from '$lib/types';
	import { goto } from '$app/navigation';

	export let data: {
		interaction: Interaction;
	};

	function volverAlListado() {
		goto('/');
	}
</script>

<section class="mx-auto max-w-4xl px-6 py-8">
	<h1 class="mb-6 text-2xl font-bold text-gray-800">
		ID de la interaccion: #{data.interaction.id}
	</h1>

	<InteractionDetail interaction={data.interaction} on:evaluacionGuardada={volverAlListado} />

	<button on:click={volverAlListado} class="mt-8 text-sm text-blue-600 hover:underline">
		← Volver al listado
	</button>
</section>
