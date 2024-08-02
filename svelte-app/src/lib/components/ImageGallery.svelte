<script lang="ts">
	let { onImageClick, images }: { onImageClick: (image: string) => void; images: Array<{ image: string; name: string; size: string }> } = $props();
</script>

<div class="my-10 flex w-full flex-col gap-4 text-center font-inter">
	<h1 class="block text-2xl font-medium leading-6 text-gray-900">Uploaded photos</h1>
	<div class="mx-auto h-full min-h-[200px] w-[90%] max-w-7xl rounded-lg bg-gray-100 px-4 py-8 sm:px-6 lg:px-8">
		{#if images.length > 0}
			<ul role="list" class="grid grid-cols-2 gap-x-4 gap-y-8 sm:grid-cols-3 sm:gap-x-6 lg:grid-cols-4 xl:gap-x-8">
				{#each images as { image, name, size }}
					<li class="relative">
						<button
							onclick={() => onImageClick(image)}
							class="group aspect-h-7 aspect-w-10 block w-full overflow-hidden rounded-lg bg-gray-100 focus-within:ring-2 focus-within:ring-indigo-500 focus-within:ring-offset-2 focus-within:ring-offset-gray-100"
						>
							<img src={image} alt="" class="pointer-events-none object-cover group-hover:opacity-75" loading="lazy" />
						</button>
						<p class="pointer-events-none mt-2 block truncate text-sm font-medium uppercase text-gray-900">{name}</p>
						<p class="pointer-events-none block text-sm font-medium text-gray-500">{Math.floor(parseInt(size) / 1000)} KB</p>
					</li>
				{/each}
			</ul>
		{:else}
			<h1 class="mt-10 block w-full text-center text-2xl font-medium leading-6 text-gray-900">No images uploaded yet.</h1>
		{/if}
	</div>
</div>
