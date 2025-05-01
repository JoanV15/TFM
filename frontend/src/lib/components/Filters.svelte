<script lang="ts">
	import { createEventDispatcher } from 'svelte';

	const dispatch = createEventDispatcher();

	export let availableModels: string[] = [];
	export let availableTags: string[] = [];

	let rating: string = '';
	let score: string = '';
	let model = '';
	let tag = '';
	let dateFrom = '';
	let dateTo = '';
	let search = '';

	function applyFilters() {
		dispatch('filterchange', {
			rating: rating !== '' ? parseInt(rating) : null,
			score: score !== '' ? (score === '-1' ? 'null' : parseInt(score)) : null,
			model: model || null,
			tag: tag || null,
			dateFrom,
			dateTo,
			search
		});
	}

	function resetFilters() {
		rating = '';
		score = '';
		model = '';
		tag = '';
		dateFrom = '';
		dateTo = '';
		search = '';

		dispatch('filterchange', {
			rating: null,
			score: null,
			model: null,
			tag: null,
			dateFrom: '',
			dateTo: '',
			search: ''
		});
	}
</script>

<div class="mb-4 space-y-4 rounded-xl bg-gray-50 p-4 shadow">
	<div class="flex flex-wrap items-end gap-4">
		<!-- Rating -->
		<div>
			<label for="rating" class="block text-sm text-gray-700">Thumbs (👍👎)</label>
			<select id="rating" bind:value={rating} class="mt-1 w-full rounded border px-3 py-2">
				<option value="">Todas</option>
				<option value="1">👍</option>
				<option value="0">–</option>
				<option value="-1">👎</option>
			</select>
		</div>

		<!-- Score -->
		<div>
			<label for="score" class="block text-sm text-gray-700">Score</label>
			<select id="score" bind:value={score} class="mt-1 w-full rounded border px-3 py-2">
				<option value="">Todos</option>
				<option value="-1">– Sin evaluar</option>
				{#each Array.from({ length: 11 }) as _, i}
					<option value={i}>{i}</option>
				{/each}
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
			<label for="search-text" class="block text-sm text-gray-700"
				>Búsqueda por frase o palabras</label
			>
			<input
				id="search-text"
				type="text"
				placeholder="Buscar..."
				bind:value={search}
				on:keydown={(e) => e.key === 'Enter' && applyFilters()}
				class="mt-1 w-full rounded border px-3 py-2"
			/>
		</div>

		<div class="flex gap-2">
			<button
				on:click={applyFilters}
				class="rounded bg-blue-600 px-4 py-2 text-white transition hover:bg-blue-700"
			>
				Aplicar
			</button>

			<button
				on:click={resetFilters}
				type="button"
				class="rounded border border-gray-300 px-4 py-2 text-gray-700 transition hover:bg-gray-100"
			>
				Limpiar filtros
			</button>
		</div>
	</div>
</div>
