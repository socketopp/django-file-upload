import { schema } from '$lib/schema';
import type { PageServerLoad } from './$types';
import { fail, setError, superValidate, withFiles } from 'sveltekit-superforms';
import { zod } from 'sveltekit-superforms/adapters';
import { type Actions } from '@sveltejs/kit';

import { MEDIA_URL, BASE_URL } from '$lib/constants';

export const load: PageServerLoad = async () => {
	const form = await superValidate(zod(schema));
	let images = [];
	try {
		const response = await fetch(`${BASE_URL}/api/list`);
		if (!response.ok) throw new Error('Failed to fetch images');
		const data = await response.json();
		if (!data.length) return { form, images: [] };
		images = data.map((image: { image: string }) => ({
			...image,
			image: `${MEDIA_URL}${image.image}`
		}));
		return { form, images };
	} catch (e) {
		console.log('PageServerLoad', e);
		return { form, images: [] };
	}
};

export const actions: Actions = {
	submit: async ({ request }) => {
		const formData = await request.formData();
		const form = await superValidate(formData, zod(schema));
		if (!form.valid) {
			return fail(400, withFiles({ form }));
		}

		const uploadFormData = new FormData();
		const file: File | null = form.data.image;
		if (!file) {
			return setError(form, 'image', 'Please upload a file.');
		}
		uploadFormData.append('image', file);

		try {
			const response = await fetch(`${BASE_URL}/api/upload`, {
				method: 'POST',
				body: uploadFormData,
				headers: {
					Accept: 'application/json'
				}
			});

			if (!response.ok) {
				return setError(form, 'image', 'Could not upload right now.');
			}
		} catch (error) {
			console.error('Error uploading file:', error);
		}

		return withFiles({ form });
	}
};
