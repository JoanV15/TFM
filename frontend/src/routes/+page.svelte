<script lang="ts">
	import { onMount } from 'svelte';
	import { getInteractions, getStats } from '$lib/api/api_frontend';
	import Filters from '$lib/components/Filters.svelte';
	import InteractionList from '$lib/components/InteractionList.svelte';
	import type { Interaction } from '$lib/types';
	import type { InteractionFilters } from '$lib/api/api_frontend';

	let interactions: Interaction[] = [];
	let loading = true;
	let error: string | null = null;

	let availableModels: string[] = [];
	let availableTags: string[] = [];

	let currentFilters = {
		rating: null as number | null,
		score: null as string | number | null,
		model: null as string | null,
		tag: null as string | null,
		dateFrom: '',
		dateTo: '',
		search: ''
	};

	let limit = 10;
	let offset = 0;
	let totalItems = 0;
	let currentPage = 1;

	function updatePagination(newOffset: number) {
		offset = newOffset;
		currentPage = Math.floor(offset / limit) + 1;
		loadInteractions();
	}

	async function loadStats() {
		try {
			const stats = await getStats();
			totalItems = stats.total_interactions;
			availableModels = Object.keys(stats.models_usage);
			availableTags = Object.keys(stats.tags_usage);
		} catch (err) {
			error = 'Error al cargar estadísticas.';
		}
	}

	async function loadInteractions() {
		loading = true;
		error = null;

		const filtrosAplicados: InteractionFilters = {
			limit,
			offset
		};

		if (typeof currentFilters.rating === 'number' && !isNaN(currentFilters.rating)) {
			filtrosAplicados.rating = currentFilters.rating;
		}

		if (currentFilters.score === 'null') {
			filtrosAplicados.score = 'null';
		} else if (typeof currentFilters.score === 'number' && !isNaN(currentFilters.score)) {
			filtrosAplicados.score = currentFilters.score;
		}

		if (currentFilters.model) {
			filtrosAplicados.model = currentFilters.model;
		}

		if (currentFilters.tag) {
			filtrosAplicados.tag = currentFilters.tag;
		}

		if (currentFilters.dateFrom) {
			filtrosAplicados.date_from = currentFilters.dateFrom;
		}

		if (currentFilters.dateTo) {
			filtrosAplicados.date_to = currentFilters.dateTo;
		}

		if (currentFilters.search) {
			filtrosAplicados.search = currentFilters.search;
		}

		try {
			const response = await getInteractions(filtrosAplicados);
			interactions = response;
		} catch (err) {
			error = 'No se pudieron cargar las interacciones.';
		} finally {
			loading = false;
		}
	}

	onMount(async () => {
		await loadStats();
		await loadInteractions();
	});

	function handleFilterChange(event: CustomEvent) {
		const filters = event.detail;

		currentFilters = {
			...filters,
			score:
				filters.score === 'null'
					? 'null'
					: typeof filters.score === 'string'
						? parseInt(filters.score)
						: filters.score
		};

		offset = 0;
		currentPage = 1;
		loadInteractions();
	}
</script>

<main class="mx-auto max-w-4xl px-4 py-6">
	<h1 class="mb-6 text-2xl font-bold">Historial de Interacciones</h1>

	<Filters on:filterchange={handleFilterChange} {availableModels} {availableTags} />

	{#if loading}
		<p class="text-gray-500">Cargando interacciones...</p>
	{:else if error}
		<p class="text-red-600">{error}</p>
	{:else if interactions.length === 0}
		<p class="text-gray-500">No hay interacciones registradas.</p>
	{:else}
		<div>
			<InteractionList {interactions} />

			<p class="mt-2 text-sm text-gray-500">
				Mostrando {offset + 1}–{Math.min(offset + limit, totalItems)} de {totalItems} interacciones
			</p>

			<div class="mt-6 flex items-center justify-between text-sm text-gray-600">
				<button
					on:click={() => updatePagination(offset - limit)}
					class="rounded bg-gray-200 px-3 py-1 hover:bg-gray-300 disabled:opacity-50"
					disabled={offset === 0}
				>
					← Anterior
				</button>

				<span>Página {currentPage}</span>

				<button
					on:click={() => updatePagination(offset + limit)}
					class="rounded bg-gray-200 px-3 py-1 hover:bg-gray-300 disabled:opacity-50"
					disabled={interactions.length < limit}
				>
					Siguiente →
				</button>
			</div>
		</div>
	{/if}
</main>
