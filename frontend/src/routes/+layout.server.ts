import type { LayoutServerLoad } from './$types';

export const load = (async (request) => {
	return {
		loggedIn: request.cookies.get('access_token') ? true : false
	};
}) satisfies LayoutServerLoad;
