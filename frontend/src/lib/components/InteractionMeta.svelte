<script lang="ts">
	import type { Interaction } from '$lib/types';
	export let interaction: Interaction;
</script>

<div class="mt-3 space-y-3 rounded-xl border bg-gray-50 p-4 text-sm text-gray-700">
	<div>
		<strong>⭐ Score:</strong>
		<span>{interaction.score ?? '--'}</span>
	</div>

	<div>
		<strong>📈 RAG Score:</strong>
		<span>{interaction.rag_score !== undefined ? interaction.rag_score.toFixed(2) : '--'}</span>
	</div>

	<div>
		<strong>🏷️ Tags:</strong>
		{#if interaction.tags && interaction.tags.length > 0}
			<div class="mt-1 flex flex-wrap gap-2">
				{#each interaction.tags as tag}
					<span class="rounded-full bg-blue-100 px-2 py-1 text-xs text-blue-800">{tag}</span>
				{/each}
			</div>
		{:else}
			<span class="text-gray-500">--</span>
		{/if}
	</div>

	<div>
		<strong>🗒️ Notas:</strong>
		<p class="mt-1 text-sm whitespace-pre-wrap text-gray-600">
			{interaction.notes ?? '--'}
		</p>
	</div>
</div>
