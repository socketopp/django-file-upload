<script lang="ts">
	import { scale } from 'svelte/transition';
	import { quintInOut } from 'svelte/easing';
	import { clickOutside } from '$lib/clickOutside';

	let { previewImage, onClose }: { previewImage: string | null | undefined; onClose: () => void } = $props();

	function handleOutclick() {
		onClose();
	}

	function handleEscape(event: KeyboardEvent) {
		if (event.key === 'Escape') {
			previewImage = null;
		}
	}
</script>

<svelte:window on:keydown={handleEscape} />

{#if previewImage}
	<div class="relative z-[99999999]" aria-labelledby="modal-title" role="dialog" aria-modal="true">
		<div class="fixed inset-0 backdrop-blur-sm"></div>
		<div class="fixed inset-0 z-10 w-screen overflow-y-auto" transition:scale={{ duration: 500, opacity: 0, start: 0, easing: quintInOut }}>
			<div class="flex min-h-full items-center justify-center p-4 text-center">
				<div
					use:clickOutside
					onoutclick={handleOutclick}
					class="relative w-full transform overflow-hidden rounded-xl border-[1px] text-left shadow-lg transition-all sm:my-8 sm:max-w-lg"
				>
					<img loading="lazy" src={previewImage} alt="previewImage" class="h-full w-full" />
				</div>
			</div>
		</div>
	</div>
{/if}
