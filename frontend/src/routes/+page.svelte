<script lang="ts">
	import Filters from '$lib/components/Filters.svelte';
	import InteractionList from '$lib/components/InteractionList.svelte';
	import type { Interaction } from '$lib/types';
/*
	 let allInteractions: Interaction[] = [
		{
			id: 1,
			prompt: '¿Qué es la inflación?',
			response: 'La inflación es el aumento generalizado de los precios...',
			thumbs: 'up',
			timestamp: '2025-03-28'
		},
		{
			id: 2,
			prompt: 'Explica el modelo IS-LM',
			response: 'El modelo IS-LM representa el equilibrio en los mercados de bienes y dinero...',
			thumbs: 'down',
			timestamp: '2025-03-27'
		}
	]; 

	let filteredInteractions = [...allInteractions];

	function handleFilterChange(event: CustomEvent) {
		const { thumbs, dateFrom, dateTo, search } = event.detail;

		filteredInteractions = allInteractions.filter((item) => {
			const matchThumb = thumbs === 'all' || item.thumbs === thumbs;
			const matchText =
				item.prompt.toLowerCase().includes(search.toLowerCase()) ||
				item.response.toLowerCase().includes(search.toLowerCase());

			const matchFrom = dateFrom ? item.timestamp >= dateFrom : true;
			const matchTo = dateTo ? item.timestamp <= dateTo : true;

			return matchThumb && matchText && matchFrom && matchTo;
		});
	}
</script>

*/
<section class="mx-auto max-w-5xl p-6">
	/*
	<h1 class="mb-4 text-2xl font-bold">Interacciones registradas</h1>

	<Filters on:filterchange={handleFilterChange} />

	<InteractionList interactions={filteredInteractions} />
	*/
	<h1>Hola Anna</h1>
</section>
