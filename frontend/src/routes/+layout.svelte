<script lang="ts">
	import { NotebookText } from 'lucide-svelte';
	import '../app.css';
	import { onMount } from 'svelte';
	import NotificationPermission from '$lib/NotificationPermission.svelte';

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
		<NotificationPermission />
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
