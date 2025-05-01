<script lang="ts">
	import InteractionCard from '$lib/components/InteractionCard.svelte';
	import type { Interaction } from '$lib/types';

	export let interactions: Interaction[] = [];
</script>

<section class="space-y-4 px-4 py-2">
	{#if interactions.length > 0}
		<p class="text-sm text-gray-500">
			{interactions.length} interacciones encontradas
		</p>
		{#each interactions as interaction (interaction.id)}
			<InteractionCard {interaction} />
		{/each}
	{:else}
		<p class="mt-8 text-center text-gray-400">No hay interacciones disponibles aún.</p>
	{/if}
</section>
