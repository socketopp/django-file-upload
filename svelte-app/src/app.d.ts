// See https://kit.svelte.dev/docs/types#app
// for information about these interfaces
declare global {
	namespace App {
		// interface Error {}
		// interface Locals {}
		// interface PageData {}
		// interface PageState {}
		// interface Platform {}
	}
	declare namespace svelteHTML {
		interface HTMLAttributes<T> {
			onoutclick?: CompositionEventHandler<T>;
		}
	}
	declare namespace svelte.JSX {
		interface HTMLProps<T> {
			onoutclick?: (e: CustomEvent) => void;
		}
	}
}

export {};
