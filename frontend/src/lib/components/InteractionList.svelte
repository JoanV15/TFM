<script lang="ts">
	import InteractionCard from '$lib/components/InteractionCard.svelte';
	import type { Interaction } from '$lib/types';
	import { exportInteractions } from '$lib/api/api_frontend';
	import { syncWebuiDB } from '$lib/api/api_frontend';

	export let interactions: Interaction[] = [];

	let successMessage = '';
	let errorMessage = '';

	async function descargarJSON() {
		try {
			const result = await exportInteractions();
			successMessage = `✅ ${result.evaluated_ids.length} exportadas: ${result.evaluated_ids.join(', ')}`;
			errorMessage =
				result.skipped_count > 0
					? `⚠️ ${result.skipped_count} interacciones no tienen score y no se exportaron.`
					: '';
			setTimeout(() => {
				successMessage = '';
				errorMessage = '';
			}, 8000);
		} catch (e) {
			errorMessage = '❌ Error al exportar interacciones.';
		}
	}

	async function sincronizarWebUI() {
		try {
			await syncWebuiDB();
			location.reload();
		} catch (err) {
			alert('Error al sincronizar con webui.db');
		}
	}
</script>

<section class="space-y-4 px-4 py-2">
	<div class="flex items-center justify-between">
		{#if interactions.length > 0}
			<p class="text-sm text-gray-500">
				{interactions.length} interacciones encontradas
			</p>
			<button on:click={sincronizarWebUI} class="ml-4 text-sm text-blue-600 hover:underline">
				🔄 Actualizar interacciones
			</button>
			<button
				class="rounded bg-blue-600 px-4 py-1 text-sm text-white hover:bg-blue-700"
				on:click={descargarJSON}
			>
				📤 Exportar JSON
			</button>
		{/if}
	</div>

	{#if successMessage}
		<div class="mt-2 rounded bg-blue-100 px-4 py-2 text-sm text-blue-800">
			{successMessage}
		</div>
	{/if}

	{#if errorMessage}
		<div class="mt-2 rounded bg-red-100 px-4 py-2 text-sm text-red-800">
			{errorMessage}
		</div>
	{/if}

	{#each interactions as interaction (interaction.id)}
		<InteractionCard {interaction} />
	{/each}

	{#if interactions.length === 0}
		<p class="mt-8 text-center text-gray-400">No hay interacciones disponibles aún.</p>
	{/if}
</section>
