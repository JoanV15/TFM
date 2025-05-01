<script lang="ts">
	import InteractionDetail from '$lib/components/InteractionDetail.svelte';
	import type { Interaction } from '$lib/types';
	import { goto } from '$app/navigation';

	export let data: {
		interaction: Interaction;
	};
</script>

<section class="mx-auto max-w-4xl px-6 py-8">
	<h1 class="mb-6 text-2xl font-bold text-gray-800">
		Detalle de la interacción #{data.interaction.id}
	</h1>

	<InteractionDetail interaction={data.interaction} />

	<button on:click={() => goto('/')} class="mt-8 text-sm text-blue-600 hover:underline">
		← Volver al listado
	</button>
</section>
