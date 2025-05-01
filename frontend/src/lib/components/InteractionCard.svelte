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
		class="flex w-full items-center justify-between text-left focus:ring-2 focus:ring-blue-400 focus:outline-none"
	>
		<div>
			<p class="text-sm font-semibold text-gray-800">
				{interaction.role === 'user' ? '🧑 Usuario' : '🤖 Asistente'}
			</p>
			<p class="truncate text-base text-gray-700">{interaction.content}</p>
		</div>

		{#if interaction.rating !== undefined}
			<span class="ml-4 rounded bg-blue-100 px-2 py-1 text-sm text-blue-700">
				⭐ {interaction.rating}
			</span>
		{/if}
	</button>

	{#if interaction.model}
		<p class="mt-1 text-xs text-gray-400">🧠 Modelo: {interaction.model}</p>
	{/if}
	<p class="text-xs text-gray-400">📅 {new Date(interaction.timestamp).toLocaleString()}</p>

	{#if isOpen}
		<InteractionMeta {interaction} />
	{/if}

	<button
		on:click={() => goto(`/interaction/${interaction.id}`)}
		class="mt-4 text-sm text-blue-600 hover:underline"
	>
		Ver detalle →
	</button>
</div>
