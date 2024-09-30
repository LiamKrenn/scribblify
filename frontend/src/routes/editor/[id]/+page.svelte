<script lang="ts">
	import MdEditor from '$lib/md-editor.svelte';
	import { onMount } from 'svelte';
	import type { PageData } from './$types';
	import { SaveIcon } from 'lucide-svelte';

	export let data: PageData;

	let socket: WebSocket;

	onMount(() => {
		socket = new WebSocket('ws://localhost:8000/ws/' + data.id);

		socket.onopen = () => {
			console.log('WebSocket connection opened');
			socket.send('Hello, WebSocket!');
		};

		socket.onmessage = (event) => {
			console.log('WebSocket message received:', event.data);
		};

		socket.onclose = () => {
			console.log('WebSocket connection closed');
		};

		socket.onerror = (error) => {
			console.error('WebSocket error:', error);
		};

		return () => {
			if (socket) {
				socket.close();
			}
		};
	});

	let title = 'test';
	let changed_title = false;
</script>

<form
	on:submit={() => {
		changed_title = false; // TODO: save
	}}
	class="absolute flex w-full justify-center"
>
	<input
		on:input={() => (changed_title = true)}
		bind:value={title}
		type="text"
		class="absolute top-3 h-10 w-52 rounded bg-slate-950 px-2 py-1 outline outline-2 outline-slate-700 focus:outline-sky-500"
	/>
	{#if changed_title}
		<button
			type="submit"
			class="absolute top-3 ml-[16.5rem] rounded bg-slate-700 p-2 outline outline-2 outline-slate-700 hover:bg-slate-700/70"
		>
			<SaveIcon />
		</button>
	{/if}
</form>

<div class="h-[calc(100%-4rem)] p-[2.5%] sm:p-[5%] sm:!pt-8 lg:p-[10%]">
	<MdEditor />
</div>
