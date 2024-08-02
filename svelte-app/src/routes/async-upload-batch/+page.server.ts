import { schemaImages } from '$lib/schema';
import type { PageServerLoad } from './$types';
import { fail, setError, superValidate, withFiles } from 'sveltekit-superforms';
import { zod } from 'sveltekit-superforms/adapters';
import { type Actions } from '@sveltejs/kit';
import { BASE_URL, MEDIA_URL } from '$lib/constants';

export const load: PageServerLoad = async () => {
	const form = await superValidate(zod(schemaImages));
	let images = [];

	try {
		const response = await fetch(`${BASE_URL}/api/list`);
		if (!response.ok) throw new Error('Failed to fetch images');
		const data = await response.json();
		if (!data.length) return { form, images: [] };

		images = data
			.map((image: { image: string }) => ({
				...image,
				image: `${MEDIA_URL}${image.image}`
			}))
			.reverse();
		return { form, images };
	} catch (e) {
		console.log('Unexpected error', e);
		return { form, images: [] };
	}
};

export const actions: Actions = {
	async asyncUpload({ request }) {
		const formData = await request.formData();
		const form = await superValidate(formData, zod(schemaImages));
		if (!form.valid) {
			return fail(400, withFiles({ form }));
		}
		const uploadFormData = new FormData();
		const images: File[] | undefined = form.data.images;

		if (!images || images.length === 0) {
			return setError(form, '', 'Please upload at least one file.');
		}

		images.forEach((file) => {
			uploadFormData.append('images', file);
		});

		try {
  		const response = await fetch(`${BASE_URL}/api/async/batch/upload`, {
				method: 'POST',
				body: uploadFormData,
				headers: {
					Accept: 'application/json'
				}
			});

			if (!response.ok) {
				const text = await response.text();
				console.error('response.text', text);
				return setError(form, '', 'Could not upload files right now.');
			}
		} catch (error) {
			console.error('Error uploading files:', error);
			return setError(form, '', 'An error occurred while uploading.');
		}
		return withFiles({ form });
	}
};
