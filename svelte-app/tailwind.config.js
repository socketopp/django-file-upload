/** @type {import('tailwindcss').Config} */
export default {
	content: ['./src/**/*.{html,js,svelte,ts}'],
	theme: {
		extend: {
			fontFamily: {
				segoe: ['Segoe UI'],
				inter: ['Inter'],
				dm: ['DM Sans', 'sans-serif', 'ui-sans-serif']
			}
		}
	},
	plugins: [require('@tailwindcss/forms'), require('@tailwindcss/aspect-ratio')]
};
