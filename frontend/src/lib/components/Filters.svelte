<script lang="ts">
	import { createEventDispatcher } from 'svelte';

	const dispatch = createEventDispatcher();

	// Props desde +page.svelte
	export let availableModels: string[] = [];
	export let availableTags: string[] = [];

	let rating: 'all' | 'positive' | 'negative' = 'all';
	let model = '';
	let tag = '';
	let dateFrom = '';
	let dateTo = '';
	let search = '';

	function applyFilters() {
		dispatch('filterchange', {
			rating: rating === 'positive' ? 10 : rating === 'negative' ? 0 : null,
			model: model || null,
			tags: tag || null,
			dateFrom,
			dateTo,
			search
		});
	}
</script>

<div class="mb-4 space-y-4 rounded-xl bg-gray-50 p-4 shadow">
	<div class="flex flex-wrap items-end gap-4">
		<!-- Evaluación -->
		<div>
			<label for="rating" class="block text-sm text-gray-700">Evaluación</label>
			<select id="rating" bind:value={rating} class="mt-1 w-full rounded border px-3 py-2">
				<option value="all">Todas</option>
				<option value="positive">👍 Positivas</option>
				<option value="negative">👎 Negativas</option>
			</select>
		</div>

		<!-- Modelo -->
		<div>
			<label for="model" class="block text-sm text-gray-700">Modelo</label>
			<select id="model" bind:value={model} class="mt-1 w-full rounded border px-3 py-2">
				<option value="">Todos</option>
				{#each availableModels as m}
					<option value={m}>{m}</option>
				{/each}
			</select>
		</div>

		<!-- Etiqueta -->
		<div>
			<label for="tag" class="block text-sm text-gray-700">Etiqueta</label>
			<select id="tag" bind:value={tag} class="mt-1 w-full rounded border px-3 py-2">
				<option value="">Todas</option>
				{#each availableTags as t}
					<option value={t}>{t}</option>
				{/each}
			</select>
		</div>

		<!-- Fecha Desde -->
		<div>
			<label for="date-from" class="block text-sm text-gray-700">Desde</label>
			<input
				id="date-from"
				type="date"
				bind:value={dateFrom}
				class="mt-1 w-full rounded border px-3 py-2"
			/>
		</div>

		<!-- Fecha Hasta -->
		<div>
			<label for="date-to" class="block text-sm text-gray-700">Hasta</label>
			<input
				id="date-to"
				type="date"
				bind:value={dateTo}
				class="mt-1 w-full rounded border px-3 py-2"
			/>
		</div>

		<!-- Texto libre -->
		<div class="min-w-[200px] flex-1">
			<label for="search-text" class="block text-sm text-gray-700">Texto libre</label>
			<input
				id="search-text"
				type="text"
				placeholder="Buscar..."
				bind:value={search}
				class="mt-1 w-full rounded border px-3 py-2"
			/>
		</div>

		<!-- Botón de aplicar -->
		<button
			on:click={applyFilters}
			class="rounded bg-blue-600 px-4 py-2 text-white transition hover:bg-blue-700"
		>
			Aplicar
		</button>
	</div>
</div>
