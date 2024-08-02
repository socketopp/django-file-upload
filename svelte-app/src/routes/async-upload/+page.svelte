<script lang="ts">
	import { cn } from '$lib/utility';
	import { onMount, onDestroy } from 'svelte';
	import { schemaImages, type SchemaImages } from '$lib/schema';
	import { superForm } from 'sveltekit-superforms/client';
	import { zodClient } from 'sveltekit-superforms/adapters';
	import Dropzone from 'svelte-file-dropzone';
	import FailIcon from '$lib/icons/Fail.svelte';
	import PhotoIcon from '$lib/icons/Photo.svelte';
	import ProcessIcon from '$lib/icons/Process.svelte';
	import SuccessIcon from '$lib/icons/Success.svelte';
	import { type Image } from '$lib/types';
	import type { PageData } from './$types';
	import UploadIcon from '$lib/icons/Upload.svelte';
	import Preview from '$lib/components/Preview.svelte';

	let { data }: { data: PageData } = $props();

	let fileStatus: { [key: string]: { upload_time?: number; status: string; name: string; size: number; type: string; image: string | undefined } } = $state({});

	let files: { accepted: any[]; rejected: any[] } = $state({
		accepted: [],
		rejected: []
	});

	let previewImage: string | null | undefined = $state();

	function closePreview() {
		previewImage = null;
	}

	let socket: WebSocket | undefined = $state();

	onMount(() => {
		socket = new WebSocket('ws://localhost:8000/ws/upload/');

		socket.onopen = () => {
			console.log('Connected to WebSocket server');
		};

		socket.onmessage = (event) => {
			const data = JSON.parse(event.data);
			const { job_id, status, type, image, upload_time } = data;
			if (type !== 'send_upload_notification') return;
			if (!job_id) return;

			fileStatus[job_id] = data;
			if (image && status === 'completed') {
				fileStatus[job_id].image = image;
				fileStatus[job_id].upload_time = upload_time;
			}
		};

		socket.onclose = () => {
			console.log('Disconnected from WebSocket server');
		};

		socket.onerror = (error) => {
			console.log('WebSocket error:', error);
		};

		onDestroy(() => {
			console.log('onDestroy', socket);
			if (socket) {
				socket.close();
			}
		});
	});

	interface FileSelectEventDetail {
		acceptedFiles: File[];
		fileRejections: File[];
	}

	const { form, errors, enhance, delayed, submit } = superForm<SchemaImages>(data.form, {
		validators: zodClient(schemaImages),
		resetForm: false,
		dataType: 'json'
	});

	$effect(() => {
		if (Object.keys(fileStatus).length === 0 && data.images && data.images.length > 0) {
			fileStatus = data.images.reduce((acc: typeof fileStatus, image: Image) => {
				acc[image.job_id] = image;
				return acc;
			}, {});
		}
		if ($errors.images) {
			files.accepted = [];
		}
	});

	function handleFilesSelect(e: CustomEvent<FileSelectEventDetail>) {
		const { acceptedFiles, fileRejections } = e.detail;
		files.accepted = [...files.accepted, ...acceptedFiles];
		files.rejected = [...files.rejected, ...fileRejections];
		$form.images = [...acceptedFiles];
		submit(); // Trigger form submission
	}
</script>

<div class="flex justify-center font-inter">
	<div class="my-4 mt-[5%] w-full max-w-2xl px-4 sm:px-6 lg:px-8">
		<form action="?/asyncUpload" use:enhance method="POST" enctype="multipart/form-data">
			<Dropzone on:drop={handleFilesSelect} disableDefaultStyles={true} name="images">
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
						{:else}
							<div class="flex flex-col justify-center text-center">
								<div class="mx-auto h-12 w-12 text-gray-600">
									<PhotoIcon />
								</div>
								<div class="mt-4 flex text-sm leading-6 text-gray-600">
									<label
										for="image"
										class="relative cursor-pointer rounded-md bg-white font-semibold text-indigo-600 focus-within:outline-none focus-within:ring-2 focus-within:ring-indigo-600 focus-within:ring-offset-2 hover:text-indigo-500"
									>
										<span>Upload file(s)</span>
										<input id="images" name="images" type="file" class="sr-only" accept="image/jpg, image/png, image/jpeg, image/webp" />
									</label>
									<p class="pl-1">or drag and drop</p>
								</div>
								<p class="text-xs leading-5 text-gray-600">PNG, JPG, PNG or WEBP</p>
							</div>
						{/if}
					</div>
				</div>
			</Dropzone>

			{#if $errors?.images}<span class="text-medium font-medium text-red-500">{$errors.images[0]}</span>{/if}
		</form>
	</div>
</div>

<div class="mt-10 flex w-full flex-col gap-4 text-center font-inter">
	<h1 class="block text-2xl font-medium leading-6 text-gray-900">Uploaded photos</h1>
	<div class="mx-auto h-full min-h-[200px] w-[90%] max-w-7xl rounded-lg bg-gray-100 px-4 py-8 sm:px-6 lg:px-8">
		<div class="flex flex-col rounded-xl border bg-white shadow-sm dark:border-neutral-700 dark:bg-neutral-800">
			<div class="h-12 rounded-t-xl border-t border-gray-200 bg-gray-50 px-4 py-2 md:px-5 dark:border-neutral-700 dark:bg-white/10">
				<div class="flex flex-wrap items-center justify-between gap-x-3">
					<div>
						<span class="text-sm font-semibold text-gray-800 dark:text-white"> {Object.keys(fileStatus)?.length} uploads </span>
					</div>
				</div>
			</div>
			<div class="space-y-7 p-4 md:p-5">
				{#if Object.keys(fileStatus)?.length > 0}
					{#each Object.entries(fileStatus).reverse() as [jobId, { name, size, image, upload_time }], index}
						{@const image_src = image && typeof image === 'string' ? image : undefined}
						<div>
							<div class="flex items-center justify-between">
								<div class="flex items-center gap-x-3">
									<span class="flex size-8 items-center justify-center rounded-lg border border-gray-200 text-gray-500 dark:border-neutral-700 dark:text-neutral-500">
										<UploadIcon />
									</span>
									<div class="flex flex-row items-center gap-2">
										<button disabled={image === undefined} onclick={() => (previewImage = image_src)}>
											<p
												class={cn('text-sm font-medium text-gray-800 dark:text-white', {
													'hover:cursor-pointer': image !== undefined,
													'hover:text-blue-500': image !== undefined
												})}
											>
												{name}
											</p>
										</button>
										<p class="text-xs text-gray-500 dark:text-neutral-500">({Math.floor(size / 1000)} KB)</p>
										{#if upload_time}
											<p class="text-xs text-gray-500 dark:text-neutral-500">(Uploaded in {upload_time})</p>
										{/if}
									</div>
								</div>
								<div class="inline-flex items-center gap-x-2">
									{#if fileStatus[jobId]?.status == 'completed'}
										<SuccessIcon />
									{:else if fileStatus[jobId]?.status == 'processing'}
										<ProcessIcon />
									{:else if fileStatus[jobId]?.status == 'error'}
										<FailIcon />
									{/if}
								</div>
							</div>
						</div>
					{/each}
				{/if}
			</div>
		</div>
	</div>
</div>

<Preview {previewImage} onClose={closePreview} />
