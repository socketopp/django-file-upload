<script lang="ts">
	import ImageGallery from '$lib/components/ImageGallery.svelte';
	import Preview from '$lib/components/Preview.svelte';
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();
	let previewImage: string | null | undefined = $state();

	function closePreview() {
		previewImage = null;
	}

	function handleImageClick(image: string) {
		previewImage = image;
	}
</script>

<ImageGallery images={data.images} onImageClick={handleImageClick} />

<Preview {previewImage} onClose={closePreview} />
