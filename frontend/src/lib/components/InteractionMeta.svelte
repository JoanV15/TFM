<script lang="ts">
	import type { Interaction } from '$lib/types';
	export let interaction: Interaction;
</script>

<div class="mt-3 space-y-3 rounded-xl border bg-gray-50 p-4 text-sm text-gray-700">
	<div>
		<strong> ID:</strong>
		<span>{interaction.id ?? '--'}</span>
	</div>

	<div>
		<strong> Modelo:</strong>
		<span>{interaction.model ?? '--'}</span>
	</div>

	<div>
		<strong> Score:</strong>
		<span>{interaction.score ?? '--'}</span>
	</div>

	<div>
		<strong> Tokens / Uso:</strong>
		{#if interaction.usage}
			<p class="mt-1 text-xs text-gray-500">
				Prompt: {interaction.usage.prompt_tokens ?? '--'} | Respuesta: {interaction.usage
					.completion_tokens ?? '--'} | Total: {interaction.usage.total_tokens ?? '--'}
			</p>
		{:else}
			<span class="text-gray-500">--</span>
		{/if}
	</div>

	<div>
		<strong> Tags:</strong>
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
		<strong> Notas:</strong>
		<p class="mt-1 whitespace-pre-wrap text-sm text-gray-600">
			{interaction.notes ?? '--'}
		</p>
	</div>
</div>
