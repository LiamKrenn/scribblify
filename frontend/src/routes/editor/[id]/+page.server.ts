import type { PageServerLoad } from './$types';

export const load = (async (event) => {
	return {
		id: event.params.id
	};
}) satisfies PageServerLoad;
