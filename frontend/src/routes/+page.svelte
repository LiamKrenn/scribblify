<script lang="ts">
	import NoteListItem from '$lib/note-list-item.svelte';

	let notes: { title: string; text: string; date: string }[] = [
		{
			title: 'Note 1 Note 1 Note 1 Note 1 Note 1 Note 1 Note1 Note1 Note1 Note1 Note1 Note',
			text: '# Heading\n\nThis is the content of note 1. This is the content of note 1. This is the conteote 1. This is the conteote 1. This is the conteote 1. This is the conteote 1. This is the conteote 1. This is the content of note 1.',
			date: '2022-01-01'
		},
		{
			title: 'Note 2',
			text: '# Another Heading\n\nThis is the content of note 2. This is the content of note 1. This is the content of note 1.',
			date: '2022-01-02'
		},
		{
			title: 'Note 3',
			text: '# Yet Another Heading\n\nThis is the content of note 3. This is the content of note 1. This is the content of note 1.',
			date: '2022-01-03'
		}
	];
</script>

<div class="mx-[5%] my-6 flex flex-wrap justify-center bg-red-500 sm:mx-[10%] xl:mx-[20%]">
	{#each notes as note}
		<NoteListItem {note} />
	{/each}
</div>
