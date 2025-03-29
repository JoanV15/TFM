<script lang="ts">
	import { createEventDispatcher } from 'svelte';

	const dispatch = createEventDispatcher();

	let thumbs: 'all' | 'up' | 'down' = 'all';
	let dateFrom = '';
	let dateTo = '';
	let search = '';

	function applyFilters() {
		dispatch('filterchange', {
			thumbs,
			dateFrom,
			dateTo,
			search
		});
	}
</script>

<div class="mb-4 space-y-4 rounded-xl bg-gray-50 p-4 shadow">
	<div class="flex flex-wrap items-end gap-4">
		<div>
			<label for="thumbs" class="block text-sm text-gray-700">Thumbs</label>
			<select id="thumbs" bind:value={thumbs} class="mt-1 w-full rounded border px-3 py-2">
				<option value="all">Todos</option>
				<option value="up">👍 Positivos</option>
				<option value="down">👎 Negativos</option>
			</select>
		</div>

		<div>
			<label for="date-from" class="block text-sm text-gray-700">Desde</label>
			<input
				id="date-from"
				type="date"
				bind:value={dateFrom}
				class="mt-1 w-full rounded border px-3 py-2"
			/>
		</div>

		<div>
			<label for="date-to" class="block text-sm text-gray-700">Hasta</label>
			<input
				id="date-to"
				type="date"
				bind:value={dateTo}
				class="mt-1 w-full rounded border px-3 py-2"
			/>
		</div>

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

		<button
			on:click={applyFilters}
			class="rounded bg-blue-600 px-4 py-2 text-white transition hover:bg-blue-700"
		>
			Aplicar
		</button>
	</div>
</div>
