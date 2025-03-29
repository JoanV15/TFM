<script lang="ts">
	import type { Interaction } from '$lib/types';

	export let interaction: Interaction;
</script>

<div class="space-y-4 rounded-xl bg-white p-6 shadow">
	<!-- Prompt -->
	<div>
		<h2 class="text-lg font-semibold text-gray-800">📝 Prompt</h2>
		<p class="mt-1 text-gray-700">{interaction.prompt}</p>
	</div>

	<!-- Respuesta -->
	<div>
		<h2 class="text-lg font-semibold text-gray-800">💬 Respuesta</h2>
		<p class="mt-1 text-gray-700">{interaction.response}</p>
	</div>

	<!-- Metadata -->
	<div class="grid grid-cols-1 gap-4 text-sm text-gray-600 sm:grid-cols-2">
		<p><strong>🗓 Fecha:</strong> {interaction.timestamp}</p>
		<p>
			<strong>📊 Evaluación:</strong>
			{interaction.thumbs === 'up' ? '👍 Positiva' : '👎 Negativa'}
		</p>

		{#if interaction.score !== undefined}
			<p><strong>⭐ Puntuación:</strong> {interaction.score}/10</p>
		{/if}

		{#if interaction.rag_score !== undefined}
			<p><strong>📈 RAG Score:</strong> {interaction.rag_score.toFixed(2)}</p>
		{/if}
	</div>

	<!-- Tags -->
	{#if interaction.tags && interaction.tags.length > 0}
		<div>
			<h2 class="text-sm font-semibold text-gray-700">🏷️ Etiquetas:</h2>
			<div class="mt-1 flex flex-wrap gap-2">
				{#each interaction.tags as tag}
					<span class="rounded-full bg-blue-100 px-2 py-1 text-xs text-blue-800">{tag}</span>
				{/each}
			</div>
		</div>
	{/if}

	<!-- Notas -->
	{#if interaction.notes}
		<div>
			<h2 class="text-sm font-semibold text-gray-700">🗒️ Observaciones del evaluador:</h2>
			<p class="mt-1 text-sm text-gray-600">{interaction.notes}</p>
		</div>
	{/if}
</div>
