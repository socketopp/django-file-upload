<script lang="ts">
	import CrossIcon from '$lib/icons/Cross.svelte';
	import PhotoIcon from '$lib/icons/Photo.svelte';
	import { fileProxy, superForm } from 'sveltekit-superforms/client';
	import type { PageData } from './$types';
	import { schema, type Schema } from '$lib/schema';
	import { zodClient } from 'sveltekit-superforms/adapters';
	import Dots from '$lib/icons/Dots.svelte';
	import Preview from '$lib/components/Preview.svelte';
	import ImageGallery from '$lib/components/ImageGallery.svelte';

	let { data }: { data: PageData } = $props();
	let previewImage: string | null | undefined = $state();

	const { form, errors, enhance, reset, delayed } = superForm<Schema>(data.form, {
		validators: zodClient(schema),
		resetForm: false,
		dataType: 'json'
	});

	function closePreview() {
		previewImage = null;
	}

	function handleImageClick(image: string) {
		previewImage = image;
	}

	const file = fileProxy(form, 'image');

	async function loadImage() {
		return await createImageUrl($form.image);
	}

	export function createImageUrl(file: File) {
		return new Promise<string>((resolve) => {
			if (file) {
				const reader = new FileReader();
				reader.onload = () => {
					resolve(reader.result as string);
				};
				reader.readAsDataURL(file);
			}
		});
	}
</script>

<div class="flex justify-center font-inter">
	<div class="my-4 w-full max-w-2xl px-4 sm:px-6 lg:px-8">
		<form action="?/submit" use:enhance method="POST" enctype="multipart/form-data">
			<div class="w-full">
				<h1 class="flex h-full text-2xl font-normal text-zinc-800">Photo Upload</h1>

				<div class="mt-2 flex h-64 justify-center rounded-lg border border-dashed border-gray-900/25 px-2 py-4">
					{#if $delayed}
						<div class="flex items-center font-inter text-gray-700">
							<svg class="-ml-1 mr-3 h-5 w-5 animate-spin text-indigo-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
								<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
								<path
									class="opacity-75"
									fill="currentColor"
									d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
								></path>
							</svg>
							Processing...
						</div>
					{:else if !$form.image || $errors?.image}
						<div class="flex flex-col justify-center text-center">
							<div class="mx-auto h-12 w-12 text-gray-600">
								<PhotoIcon />
							</div>
							<div class="mt-4 flex text-sm leading-6 text-gray-600">
								<label
									for="image"
									class="relative cursor-pointer rounded-md bg-white font-semibold text-indigo-600 focus-within:outline-none focus-within:ring-2 focus-within:ring-indigo-600 focus-within:ring-offset-2 hover:text-indigo-500"
								>
									<span>Upload a file</span>
									<input bind:files={$file} id="image" name="image" type="file" class="sr-only" accept="image/jpg, image/png, image/jpeg, image/webp" />
								</label>
								<p class="pl-1">or drag and drop</p>
							</div>

							<p class="text-xs leading-5 text-gray-600">PNG, JPG, PNG or WEBP up to 10MB</p>
						</div>
					{:else if $form.image && !$errors?.image?.length}
						<div class="relative mt-2 flex h-fit min-h-[134px] w-full items-center justify-center rounded-lg border-gray-900/25 px-2 py-4">
							<button class="absolute right-5 top-2 z-[9999999] stroke-zinc-500 hover:stroke-zinc-400" onclick={() => reset()}>
								<CrossIcon />
							</button>

							<div class="group aspect-h-7 block w-full overflow-hidden rounded-lg text-center">
								{#await loadImage() then imgSrc}
									{#if imgSrc}
										<img src={imgSrc} alt="preview" class="mx-auto h-48 w-[80%] rounded-md object-cover" loading="lazy" />
									{/if}
								{/await}
							</div>
						</div>
					{/if}
				</div>
			</div>

			<div class="mt-10 flex items-center gap-2">
				<button type="submit" class="min-w-[66px] rounded-md bg-indigo-500 px-2 py-2 text-white">
					{#if $delayed}
						<div class="flex justify-center stroke-white">
							<Dots />
						</div>
					{:else}
						Submit
					{/if}</button
				>
				{#if $errors.image}<span class="text-medium font-medium text-red-500">{$errors.image}</span>{/if}
			</div>
		</form>
	</div>
</div>

<ImageGallery images={data.images} onImageClick={handleImageClick} />

<Preview {previewImage} onClose={closePreview} />
