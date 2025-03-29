<script lang="ts">
	import InteractionCard from '$lib/components/InteractionCard.svelte';
	import type { Interaction } from '$lib/types';

	export let interactions: Interaction[] = []; // ← ahora es una prop
</script>

<div class="space-y-4 p-4">
	{#if interactions.length > 0}
		{#each interactions as item (item.id)}
			<InteractionCard interaction={item} />
		{/each}
	{:else}
		<p class="text-center text-gray-400">No hay interacciones disponibles aún.</p>
	{/if}
</div>
