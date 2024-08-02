<script lang="ts">
	import '../app.css';
	import Logo from '$lib/icons/Logo.svelte';
	import { page } from '$app/stores';
	const url = $page.url.pathname;
</script>

<main>
	<div class="mt-14 flex w-full items-center justify-center gap-4">
		<a data-sveltekit-reload href="/" class="hover:cursor-pointer">
			<Logo />
		</a>
	</div>
	<div class="mt-10 flex w-full flex-row justify-center gap-4 *:underline">
		<a data-sveltekit-reload class:text-blue-500={url === '/list'} href="/list"> /list</a>
		<a data-sveltekit-reload class:text-blue-500={url === '/async-upload'} href="/async-upload"> /async-upload</a>
	</div>
	<slot />
</main>
