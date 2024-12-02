<script lang="ts">
	import NoteListItem from '$lib/note-list-item.svelte';
	import { Button, buttonVariants } from '$lib/components/ui/button';
	import * as Dialog from '$lib/components/ui/dialog/index.js';
	import { Input } from '$lib/components/ui/input/index.js';
	import { Label } from '$lib/components/ui/label/index.js';
	import { onMount } from 'svelte';
	import { Plus } from 'lucide-svelte';
	import { goto } from '$app/navigation';
	import { PUBLIC_BACKEND_URL } from '$env/static/public';

	let notes: { title: string; text: string; date: string; id: number }[] = [];

	async function getNotes() {
		const res = await fetch(`${PUBLIC_BACKEND_URL}/notes?limit=999999`, {
			credentials: 'include'
		});
		notes = await res.json();
	}

	onMount(async () => {
		await getNotes();
	});

	let title = '';
	let open = false;

	async function createNote() {
		if (title == '') return;
		let res = await fetch(`${PUBLIC_BACKEND_URL}/note`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			credentials: 'include',
			body: JSON.stringify({ title: title })
		});
		title = '';
		open = false;
		await getNotes();
		goto('/editor/' + (await res.json()).id);
	}
</script>

<div class="mx-[20%] mt-6 flex justify-center">
	<Dialog.Root bind:open>
		<Dialog.Trigger
			class="flex w-full max-w-[40rem] justify-center rounded-lg bg-slate-700 p-2 hover:scale-[1.02]"
			>Create Note <Plus class="ml-1" /></Dialog.Trigger
		>
		<Dialog.Content class="sm:max-w-[425px]">
			<Dialog.Header>
				<Dialog.Title>Create Note</Dialog.Title>
			</Dialog.Header>
			<div class="grid gap-4 py-4">
				<div class="grid grid-cols-4 items-center gap-4">
					<Label for="title" class="text-right">Title</Label>
					<Input bind:value={title} id="title" placeholder="New Note" class="col-span-3 " />
				</div>
			</div>
			<Dialog.Footer>
				<Button type="submit" on:click={createNote}>Create</Button>
			</Dialog.Footer>
		</Dialog.Content>
	</Dialog.Root>
</div>

<div class="mx-[5%] my-6 flex flex-wrap justify-center sm:mx-[10%] xl:mx-[20%]">
	{#each notes as note}
		<NoteListItem {note} />
	{/each}
</div>
