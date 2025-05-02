<script lang="ts">
	import type { PageData } from './$types';
	import {
		getHeuristicMetrics,
		type HeuristicMetricsResponse,
		evaluateWithOpik,
		getInteractionById
	} from '$lib/api/api_frontend';
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';

	export let data: PageData;
	let interaction = data.interaction;

	let expected_output = '';
	let heuristicResult: HeuristicMetricsResponse | null = null;
	let error: string | null = null;
	let success = false;

	let loadingOpik = false;

	async function evaluarHeuristicas() {
		success = false;
		heuristicResult = null;
		error = null;

		try {
			const result = await getHeuristicMetrics({
				expected_output,
				actual_output: interaction.response
			});
			heuristicResult = result;
			success = true;
		} catch (err) {
			error = 'Error al calcular las métricas heurísticas.';
		}
	}

	async function evaluarConOpik() {
		const confirmar = confirm(
			'Esta evaluación utiliza la API de OpenAI y puede tener un coste. ¿Deseas continuar?'
		);
		if (!confirmar) return;

		loadingOpik = true;
		error = null;

		try {
			await evaluateWithOpik(interaction.id);
			interaction = await getInteractionById(interaction.id);
		} catch (err) {
			error = 'Error al evaluar con Opik.';
		} finally {
			loadingOpik = false;
		}
	}
</script>

<section class="mx-auto max-w-4xl space-y-8 px-6 py-10">
	<h1 class="text-2xl font-bold text-gray-800">
		📊 Métricas de evaluación – Interacción #{interaction.id}
	</h1>

	<!-- 🔷 TARJETA MÉTRICAS AUTOMÁTICAS -->
	<div class="rounded-xl border border-blue-300 bg-blue-50 p-6 shadow">
		<div class="flex items-center justify-between">
			<h2 class="text-lg font-semibold text-blue-800">Métricas automáticas (LLM-as-a-Judge)</h2>
			<button
				on:click={evaluarConOpik}
				class="rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700 disabled:opacity-50"
				disabled={loadingOpik}
			>
				{loadingOpik ? 'Evaluando...' : 'Evaluar con Opik'}
			</button>
		</div>

		{#if loadingOpik}
			<div class="mt-4 h-3 w-full overflow-hidden rounded-full bg-blue-100">
				<div class="h-full w-full animate-pulse bg-blue-500"></div>
			</div>
		{/if}

		<ul class="mt-4 space-y-1 text-sm text-gray-800">
			<li>
				<strong>Hallucination:</strong>
				{interaction.hallucination ?? '—'}
				<span class="block text-xs text-gray-500">Detecta si el modelo inventa información.</span>
			</li>
			<li>
				<strong>Moderation:</strong>
				{interaction.moderation ?? '—'}
				<span class="block text-xs text-gray-500"
					>Evalúa si la respuesta infringe normas de contenido.</span
				>
			</li>
			<li>
				<strong>Context Precision:</strong>
				{interaction.context_precision ?? '—'}
				<span class="block text-xs text-gray-500"
					>Qué parte de la respuesta es precisa respecto al contexto dado.</span
				>
			</li>
			<li>
				<strong>Context Recall:</strong>
				{interaction.context_recall ?? '—'}
				<span class="block text-xs text-gray-500"
					>Qué parte del contexto relevante fue utilizada por el modelo.</span
				>
			</li>
			<li>
				<strong>Usefulness:</strong>
				{interaction.usefulness ?? '—'}
				<span class="block text-xs text-gray-500">¿La respuesta es útil para el usuario?</span>
			</li>
			<li>
				<strong>Answer Relevance:</strong>
				{interaction.answer_relevance ?? '—'}
				<span class="block text-xs text-gray-500"
					>¿La respuesta es relevante frente al input o pregunta?</span
				>
			</li>
			<li>
				<strong>G-Eval:</strong>
				{interaction.g_eval ?? '—'}
				<span class="block text-xs text-gray-500"
					>Evaluación global basada en instrucciones personalizadas.</span
				>
			</li>
		</ul>
	</div>

	<!-- 🟨 TARJETA MÉTRICAS HEURÍSTICAS -->
	<div class="space-y-4 rounded-xl border border-yellow-300 bg-yellow-50 p-6 shadow">
		<h2 class="text-lg font-semibold text-yellow-800">
			Métricas heurísticas (comparación con respuesta esperada)
		</h2>

		<label class="block text-sm font-medium text-gray-700">
			Introduce la respuesta esperada:
			<textarea
				bind:value={expected_output}
				rows="4"
				class="mt-1 w-full rounded border px-3 py-2"
				placeholder="Escribe aquí la salida esperada del modelo..."
			></textarea>
		</label>

		<button
			on:click={evaluarHeuristicas}
			disabled={expected_output.trim() === ''}
			class="rounded bg-yellow-600 px-4 py-2 text-white hover:bg-yellow-700 disabled:opacity-50"
		>
			Evaluar métricas heurísticas
		</button>

		{#if success}
			<p class="text-sm text-yellow-800">Evaluación completada con éxito. Resultados:</p>
		{/if}

		{#if error}
			<p class="text-sm text-red-600">{error}</p>
		{/if}

		{#if heuristicResult}
			<div class="mt-4 space-y-2 text-sm text-gray-700">
				<p>
					<strong>Equals:</strong>
					{heuristicResult.equals ? '✅' : '❌'}
					<span class="block text-xs text-gray-500"
						>Compara si la respuesta es exactamente igual a la esperada.</span
					>
				</p>
				<p>
					<strong>Contains:</strong>
					{heuristicResult.contains ? '✅' : '❌'}
					<span class="block text-xs text-gray-500"
						>Verifica si la respuesta contiene el texto esperado.</span
					>
				</p>
				<p>
					<strong>RegexMatch:</strong>
					{heuristicResult.regexmatch ? '✅' : '❌'}
					<span class="block text-xs text-gray-500"
						>Evalúa si la respuesta cumple con un patrón de expresión regular.</span
					>
				</p>
				<p>
					<strong>Is JSON:</strong>
					{heuristicResult.isjson ? '✅' : '❌'}
					<span class="block text-xs text-gray-500"
						>Comprueba si la respuesta es un JSON válido.</span
					>
				</p>
				<p>
					<strong>Levenshtein Ratio:</strong>
					{heuristicResult.levenshtein}
					<span class="block text-xs text-gray-500"
						>Medida de similitud textual entre respuesta y esperado (0–1).</span
					>
				</p>
			</div>
		{/if}
	</div>
	<div class="mt-8 flex justify-between">
		<!-- Botón izquierdo: volver -->
		<button on:click={() => history.back()} class="text-sm text-blue-600 hover:underline">
			← Volver al listado
		</button>

		<!-- Botón derecho: ir a detalles -->
		<button
			on:click={() => goto(`/interaction/${interaction.id}`)}
			class="text-sm text-blue-600 hover:underline"
		>
			📄 Ver detalles
		</button>
	</div>
</section>
