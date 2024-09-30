<script lang="ts">
	import NoteListItem from '$lib/note-list-item.svelte';
	import { onMount } from 'svelte';

	let notes: { title: string; text: string; date: string }[] = [];

	onMount(async () => {
		const res = await fetch('http://localhost:8000/notes');
		notes = await res.json();
	});
</script>

<div class="mx-[5%] my-6 flex flex-wrap justify-center sm:mx-[10%] xl:mx-[20%]">
	{#each notes as note}
		<NoteListItem {note} />
	{/each}
</div>
