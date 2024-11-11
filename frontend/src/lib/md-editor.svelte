<script>
	import { Carta, MarkdownEditor } from 'carta-md';
	import 'carta-md/default.css'; /* Default theme */
	import DOMPurify from 'isomorphic-dompurify';

	export let value = '';

	const carta = new Carta({
		sanitizer: DOMPurify.sanitize,
		theme: 'github-dark'
	});
</script>

<MarkdownEditor {carta} bind:value />

<style>
	/* Set your monospace font (Required to have the editor working correctly!) */
	:global(.carta-font-code) {
		font-family: '...', monospace;
		font-size: 1.1rem;
	}
</style>
