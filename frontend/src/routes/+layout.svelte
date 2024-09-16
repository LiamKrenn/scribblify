<script lang="ts">
	import { NotebookText } from 'lucide-svelte';
	import '../app.css';
</script>

<div class="flex h-full w-full flex-col">
	<div class="flex h-16 w-full items-center border-b-2 border-slate-800 p-2">
		<a href="/" class="flex items-center rounded-xl p-2 hover:bg-slate-800">
			<NotebookText class="h-8 w-8" />
			<p class="ml-2 text-3xl">scribblify</p>
		</a>
	</div>
	<slot></slot>
</div>

<style>
	:global(*) {
		transition-duration: 150ms;
	}
</style>
