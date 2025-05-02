<script lang="ts">
	import InteractionDetail from '$lib/components/InteractionDetail.svelte';
	import type { Interaction } from '$lib/types';
	import { goto } from '$app/navigation';

	export let data: {
		interaction: Interaction;
	};

	let interaction = data.interaction;

	function volverAlListado() {
		goto('/');
	}
</script>

<section class="mx-auto max-w-4xl px-6 py-8">
	<h1 class="mb-6 text-2xl font-bold text-gray-800">
		ID de la interaccion: #{data.interaction.id}
	</h1>

	<InteractionDetail interaction={data.interaction} on:evaluacionGuardada={volverAlListado} />
	<div class="mt-8 flex justify-between">
		<!-- Botón izquierdo: volver -->
		<button on:click={volverAlListado} class="text-sm text-blue-600 hover:underline">
			← Volver al listado
		</button>

		<!-- Botón derecho: ir a métricas -->
		<button
			on:click={() => goto(`/metrics/${data.interaction.id}`)}
			class="text-sm text-blue-600 hover:underline"
		>
			📊 Ver métricas de evaluación
		</button>
	</div>
</section>
