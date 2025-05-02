<script lang="ts">
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { getInteractionById, postEvaluation } from '$lib/api/api_frontend';
	import type { Interaction } from '$lib/types';
	import { createEventDispatcher } from 'svelte';

	const dispatch = createEventDispatcher();

	export let interaction: Interaction;
	let loading = true;
	let error: string | null = null;

	let score: string = '';
	let rating: string = '';
	let notes: string = '';
	let tags: string = '';

	const id = $page.params.id;

	onMount(async () => {
		try {
			interaction = await getInteractionById(id);
			score =
				interaction.score !== null && interaction.score !== undefined
					? String(interaction.score)
					: '';
			rating =
				interaction.rating !== undefined && interaction.rating !== null
					? String(interaction.rating)
					: '';
			notes = interaction.notes ?? '';
			tags = interaction.tags?.join(', ') ?? '';
		} catch (err) {
			error = 'Error al cargar la interacción.';
		} finally {
			loading = false;
		}
	});

	async function guardarEvaluacion() {
		try {
			await postEvaluation(id, {
				score:
					score !== '' && !isNaN(Number(score)) && Number(score) >= 0 && Number(score) <= 10
						? Number(score)
						: undefined,
				rating: rating !== '' ? parseInt(rating) : undefined,
				notes,
				tags: tags
					.split(',')
					.map((t) => t.trim())
					.filter(Boolean)
			});
			dispatch('evaluacionGuardada'); // Notifica al componente padre
		} catch {
			error = 'Error al guardar la evaluación.';
		}
	}
</script>

{#if loading}
	<p class="text-gray-500">Cargando interacción...</p>
{:else if error}
	<p class="text-red-600">{error}</p>
{:else}
	<div class="space-y-6 rounded-xl bg-white p-6 text-sm text-gray-800 shadow">
		<!-- Prompt -->
		<div>
			<h2 class="text-lg font-semibold">🧑 Prompt</h2>
			<p class="mt-1 whitespace-pre-wrap text-gray-700">{interaction.prompt}</p>
		</div>

		<!-- Respuesta -->
		<div>
			<h2 class="text-lg font-semibold">🤖 Respuesta del modelo</h2>
			<p class="mt-1 whitespace-pre-wrap text-gray-700">{interaction.response}</p>
		</div>

		<!-- Metadatos -->
		<div class="grid grid-cols-1 gap-4 text-gray-600 sm:grid-cols-2">
			<p><strong>🧠 Modelo:</strong> {interaction.model ?? '--'}</p>
			<p><strong>🗓 Fecha:</strong> {new Date(interaction.timestamp).toLocaleString()}</p>

			{#if interaction.usage}
				<p>
					<strong>📦 Tokens usados:</strong>
					{interaction.usage.total_tokens ?? '--'} (Prompt: {interaction.usage.prompt_tokens ??
						'--'}, Completion: {interaction.usage.completion_tokens ?? '--'})
				</p>
			{/if}
		</div>

		<!-- Evaluación editable -->
		<div class="grid grid-cols-1 gap-4 sm:grid-cols-3">
			<div>
				<label for="score" class="block text-sm font-medium text-gray-700">⭐ Score (0–10)</label>
				<input
					id="score"
					type="number"
					min="0"
					max="10"
					bind:value={score}
					class="mt-1 w-full rounded border px-3 py-2"
				/>
				{#if score !== '' && (isNaN(Number(score)) || Number(score) < 0 || Number(score) > 10)}
					<p class="mt-1 text-xs text-red-600">⚠️ Score debe estar entre 0 y 10.</p>
				{/if}
			</div>

			<div>
				<label for="rating" class="block text-sm font-medium text-gray-700">👍 Evaluación</label>
				<select id="rating" bind:value={rating} class="mt-1 w-full rounded border px-3 py-2">
					<option value="1">👍 Aprobado</option>
					<option value="0">– Neutral</option>
					<option value="-1">👎 Rechazado</option>
				</select>
			</div>

			<div>
				<label for="tags" class="block text-sm font-medium text-gray-700">🏷️ Tags (coma)</label>
				<input
					id="tags"
					type="text"
					bind:value={tags}
					placeholder="ej: macroeconomía, confuso"
					class="mt-1 w-full rounded border px-3 py-2"
				/>
			</div>
		</div>

		<!-- Notas -->
		<div>
			<label for="notes" class="block text-sm font-medium text-gray-700"
				>🗒️ Notas del evaluador</label
			>
			<textarea id="notes" bind:value={notes} rows="4" class="mt-1 w-full rounded border px-3 py-2"
			></textarea>
		</div>

		<!-- Botón guardar -->
		<div class="pt-2">
			<button
				on:click={guardarEvaluacion}
				class="rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700 disabled:opacity-50"
				disabled={score !== '' && (isNaN(Number(score)) || Number(score) < 0 || Number(score) > 10)}
			>
				Guardar evaluación
			</button>
		</div>
	</div>
{/if}
