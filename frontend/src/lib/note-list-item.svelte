<script lang="ts">
	export let note: { title: string; text: string; date: string; id: number };
</script>

<a
	href="/editor/{note.id}"
	class="m-2 flex h-44 w-48 cursor-pointer flex-col overflow-hidden rounded-xl bg-slate-700 px-3 py-2 hover:scale-[1.02]"
>
	<h2 class="shrink-0 truncate text-2xl">{note.title}</h2>
	<p class="note-text my-1.5 h-full max-h-full text-slate-300">{note.text}</p>
	<p class="text-nowrap text-right text-slate-400">{note.date}</p>
</a>

<style>
	.note-text {
		display: -webkit-box;
		text-overflow: ellipsis;
		overflow: hidden;
		-webkit-box-orient: vertical;
		-webkit-line-clamp: 4;
	}
</style>
