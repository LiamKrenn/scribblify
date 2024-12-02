<script lang="ts">
	import MdEditor from '$lib/md-editor.svelte';
	import { onMount } from 'svelte';
	import type { PageData } from './$types';
	import { SaveIcon, SlidersHorizontal } from 'lucide-svelte';
	import { Input } from '$lib/components/ui/input/index.js';
	import { Label } from '$lib/components/ui/label/index.js';
	import * as Dialog from '$lib/components/ui/dialog/index.js';
	import { Button, buttonVariants } from '$lib/components/ui/button';

	export let data: PageData;

	let socket: WebSocket;

	let sendText = (text: string) => {};

	let block = false;

	onMount(() => {
		// getAllUsers();
		value = '';

		socket = new WebSocket('wss://localhost:8002/ws/' + data.id);

		socket.onopen = () => {
			console.log('WebSocket connection opened');
		};

		socket.onmessage = (event) => {
			console.log('WebSocket message received:', event.data);
			block = true;
			value = event.data;
		};

		socket.onclose = () => {
			console.log('WebSocket connection closed');
		};

		socket.onerror = (error) => {
			console.error('WebSocket error:', error);
		};

		sendText = (text: string) => {
			block = true;
			socket.send(text);
		};

		return () => {
			if (socket) {
				socket.close();
			}
		};
	});

	let title = 'test';
	let changed_title = false;
	let value = '';

	$: if (value) {
		if (block) {
			block = false;
		} else {
			sendText(value);
		}
	}

	let addemail = '';
	let adderror = '';

	async function addUser() {
		adderror = '';
		const res_user = await fetch(
			'https://localhost:8002/user?email=' + addemail.replace('@', '%40'),
			{ credentials: 'include' }
		);
		if (res_user.status !== 200) {
			adderror = 'User not found';
			return;
		}
		const json_user = await res_user.json();

		const res = await fetch('https://localhost:8002/note_access/', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			credentials: 'include',
			body: JSON.stringify({
				note_id: data.id,
				user_id: json_user.id
			})
		});
		await getAllUsers();
	}

	let open = false;

	let useraccess: any[] = [];

	async function getAllUsers() {
		const res = await fetch('https://localhost:8002/note_access/' + data.id, {
			credentials: 'include'
		});
		const json = await res.json();
		useraccess = json;
	}
</script>

<form
	on:submit={() => {
		changed_title = false; // TODO: save
	}}
	class="my-4 flex w-full justify-center"
>
	<input
		on:input={() => (changed_title = true)}
		bind:value={title}
		type="text"
		class="h-10 w-52 rounded bg-slate-950/50 px-2 py-1 outline outline-2 outline-slate-700 focus:outline-sky-500"
	/>
	{#if changed_title}
		<button
			type="submit"
			class="absolute ml-[16.5rem] rounded bg-slate-700 p-2 outline outline-2 outline-slate-700 hover:bg-slate-700/70"
		>
			<SaveIcon />
		</button>
	{/if}

	<Dialog.Root bind:open>
		<Dialog.Trigger
			class="absolute right-[2.5%] mr-2 flex h-10 justify-center rounded-lg bg-slate-700 p-2 hover:scale-[1.02] sm:right-[5%] lg:right-[10%]"
			><SlidersHorizontal /></Dialog.Trigger
		>
		<Dialog.Content class="sm:max-w-[425px]">
			<Dialog.Header>
				<Dialog.Title class="flex items-center"
					><SlidersHorizontal class="mr-4" />Manage Access</Dialog.Title
				>
			</Dialog.Header>
			<div>
				<Label for="email" class="text-right">Add user with E-Mail</Label>
				<div class="mb-2 mt-1 flex">
					<Input bind:value={addemail} id="email" placeholder="example@email.com" type="email" />
					<Button
						variant="secondary"
						class="ml-2"
						on:click={async () => {
							await addUser();
						}}>Add</Button
					>
				</div>
				<p class="mb-2 text-red-400">{adderror}</p>
				{#if useraccess.length != 0}
					<Label for="email" class="text-right">User that already have access</Label>
					{#each useraccess as user}
						{user}
					{/each}
				{/if}
			</div>
		</Dialog.Content>
	</Dialog.Root>
</form>

<div class="h-[calc(100%-10rem)] px-[2.5%] sm:px-[5%] lg:px-[10%]">
	<MdEditor bind:value />
</div>
