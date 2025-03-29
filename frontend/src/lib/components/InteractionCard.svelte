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

<div class="rounded-2xl border p-4 shadow transition hover:shadow-md">
	<button
		type="button"
		on:click={toggleDetails}
		class="flex w-full items-center justify-between text-left focus:outline-none focus:ring-2 focus:ring-blue-400"
	>
		<h2 class="text-base font-medium text-gray-800">{interaction.prompt}</h2>
		<span
			class={`rounded px-2 py-1 text-sm ${interaction.thumbs === 'up' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}
		>
			{interaction.thumbs === 'up' ? '👍 Positiva' : '👎 Negativa'}
		</span>
	</button>

	<p class="mt-2 truncate text-sm text-gray-600">{interaction.response}</p>
	<p class="mt-1 text-xs text-gray-400">📅 {interaction.timestamp}</p>

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
