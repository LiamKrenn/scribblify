<script lang="ts">
	import { NotebookText, LogIn } from 'lucide-svelte';
	import '../app.css';
	import { onMount } from 'svelte';
	import NotificationPermission from '$lib/NotificationPermission.svelte';
	import type { PageData } from './$types';

	export let data: PageData;

	onMount(() => {
		if ('serviceWorker' in navigator) {
			navigator.serviceWorker
				.register('/service-worker.js')
				.then((registration) => {
					console.log('Service Worker registered with scope:', registration.scope);
				})
				.catch((error) => {
					console.error('Service Worker registration failed:', error);
				});
		}
	});
</script>

<div class="flex h-full w-full flex-col">
	<div class="flex h-16 w-full items-center justify-between border-b-2 border-slate-800 p-2">
		<a href="/" class="flex items-center rounded-xl p-2 hover:bg-slate-800">
			<NotebookText class="h-8 w-8" />
			<p class="ml-2 text-3xl">scribblify</p>
		</a>
		<div class="flex">
			<NotificationPermission />
			{#if data.loggedIn}
				Logged In
			{:else}
				<a
					href="https://localhost:8000/login/oauth/ms"
					class="ml-2 flex h-12 items-center justify-center rounded-lg bg-sky-700 px-4"
					>Log In <LogIn class="ml-1.5" />
				</a>
			{/if}
		</div>
	</div>
	<div class="overflow-y-scroll">
		<slot></slot>
	</div>
</div>

<style>
	:global(*) {
		transition-duration: 150ms;
	}
</style>
