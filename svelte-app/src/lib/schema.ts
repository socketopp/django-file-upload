import { z } from 'zod';

const ACCEPTED_IMAGE_TYPES = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp'];

export const schema = z.object({
	image: z
		.instanceof(File, { message: 'Please upload a file.' })
		.refine((f) => f.size < 400_000, 'Max 400 kB upload size.')
		.refine((f) => ACCEPTED_IMAGE_TYPES.includes(f?.type), 'Only .jpg, .jpeg, .png and .webp formats are supported.')
});

export const schemaImages = z.object({
	images: z
		.instanceof(File, { message: 'Please upload a file.' })
		.refine((f) => f.size < 400_000, 'Max 400 kB upload size.')
		.refine((f) => ACCEPTED_IMAGE_TYPES.includes(f?.type), 'Only .jpg, .jpeg, .png and .webp formats are supported.')
		.array()
});

export type SchemaImages = z.infer<typeof schemaImages>;
export type Schema = z.infer<typeof schema>;
