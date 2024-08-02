import type { PageServerLoad } from './$types';

import { BASE_URL, MEDIA_URL } from '$lib/constants';

export const load: PageServerLoad = async () => {
	let images = [];

	try {
		const response = await fetch(`${BASE_URL}/api/list`);
		if (!response.ok) throw new Error('Failed to fetch images');
		const data = await response.json();
		images = data.map((image: { image: string }) => ({
			...image,
			image: `${MEDIA_URL}${image.image}`
		}));
		return { images };
	} catch (e) {
		console.log('Exception', e);
		return { images: [] };
	}
};
