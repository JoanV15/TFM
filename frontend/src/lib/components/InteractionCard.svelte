<script lang="ts">
	import type { Interaction } from '$lib/types';
	import InteractionMeta from '$lib/components/InteractionMeta.svelte';
	import { goto } from '$app/navigation';

	export let interaction: Interaction;

	let isOpen = false;
	function toggleDetails() {
		isOpen = !isOpen;
	}
</script>

<div class="rounded-2xl border bg-white p-4 shadow transition hover:shadow-md">
	<button
		type="button"
		on:click={toggleDetails}
		class="flex w-full items-center justify-between text-left focus:outline-none focus:ring-2 focus:ring-blue-400"
	>
		<div class="w-full">
			<p class="mb-1 text-sm font-semibold text-gray-800">
				🧾 {interaction.prompt.slice(0, 80)}{interaction.prompt.length > 80 ? '...' : ''}
			</p>
			<p class="text-sm italic text-gray-600">
				{interaction.response.slice(0, 100)}{interaction.response.length > 100 ? '...' : ''}
			</p>
		</div>

		{#if interaction.rating === 1}
			<span class="ml-4 rounded bg-green-100 px-2 py-1 text-sm text-green-700">👍</span>
		{:else if interaction.rating === -1}
			<span class="ml-4 rounded bg-red-100 px-2 py-1 text-sm text-red-700">👎</span>
		{:else}
			<span class="ml-4 rounded bg-blue-100 px-2 py-1 text-sm text-blue-700">–</span>
		{/if}
	</button>

	{#if interaction.model}
		<p class="mt-1 text-xs text-gray-400">🧠 Modelo: {interaction.model}</p>
	{/if}
	<p class="text-xs text-gray-400">📅 {new Date(interaction.timestamp).toLocaleString()}</p>

	{#if isOpen}
		<InteractionMeta {interaction} />
	{/if}

	<div class="mt-4 flex items-center justify-between text-sm">
		<span class="text-gray-500">
			Score: {interaction.score !== null && interaction.score !== undefined
				? interaction.score
				: '–'}
		</span>
		<button
			on:click={() => goto(`/interaction/${interaction.id}`)}
			class="text-blue-600 hover:underline"
		>
			Ver detalles →
		</button>
		<button
			on:click={() => goto(`/metrics/${interaction.id}`)}
			class="text-sm text-blue-600 hover:underline"
		>
			🔍 Ver métricas
		</button>
	</div>
</div>
