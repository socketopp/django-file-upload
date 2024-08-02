export function clickOutside(node: Node) {
	const handleClick = (event: Event) => {
		const target = event?.target as Node;
		if (node && !node.contains(target) && !event.defaultPrevented) {
			node.dispatchEvent(new CustomEvent('outclick', { detail: event?.target }));
		}
	};

	document.addEventListener('click', handleClick, true);

	return {
		destroy() {
			document.removeEventListener('click', handleClick, true);
		}
	};
}
