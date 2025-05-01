<script lang="ts">
	import type { Interaction } from '$lib/types';

	export let interaction: Interaction;
</script>

<div class="space-y-6 rounded-xl bg-white p-6 text-sm text-gray-800 shadow">
	<!-- Rol y contenido -->
	<div>
		<h2 class="text-lg font-semibold">🧑‍💻 Interacción</h2>
		<p class="mt-1">
			<span class="font-semibold text-gray-600">Rol:</span>
			{interaction.role === 'user' ? 'Usuario' : 'Asistente'}
		</p>
		<p class="mt-2 whitespace-pre-wrap text-gray-700">{interaction.content}</p>
	</div>

	<!-- Metadatos -->
	<div class="grid grid-cols-1 gap-4 text-gray-600 sm:grid-cols-2">
		<p><strong>🧠 Modelo:</strong> {interaction.model ?? '--'}</p>
		<p><strong>🗓 Fecha:</strong> {new Date(interaction.timestamp).toLocaleString()}</p>

		{#if interaction.rating !== undefined}
			<p><strong>📊 Evaluación:</strong> {interaction.rating}/10</p>
		{/if}

		{#if interaction.score !== undefined}
			<p><strong>⭐ Score manual:</strong> {interaction.score}/10</p>
		{/if}

		{#if interaction.rag_score !== undefined}
			<p><strong>📈 RAG Score:</strong> {interaction.rag_score.toFixed(2)}</p>
		{/if}
	</div>

	<!-- Etiquetas -->
	{#if interaction.tags && interaction.tags.length > 0}
		<div>
			<h2 class="text-sm font-semibold text-gray-700">🏷️ Etiquetas asignadas</h2>
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
			<h2 class="text-sm font-semibold text-gray-700">🗒️ Observaciones del evaluador</h2>
			<p class="mt-1 whitespace-pre-wrap text-gray-700">{interaction.notes}</p>
		</div>
	{/if}
</div>
