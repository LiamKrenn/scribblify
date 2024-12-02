<script lang="ts">
	import { PUBLIC_BACKEND_URL } from '$env/static/public';

	let username = '';
	let password = '';

	async function login() {
		console.log('login');

		let form = new FormData();

		form.append('username', username);
		form.append('password', password);

		const res = await fetch(`${PUBLIC_BACKEND_URL}/login`, {
			credentials: 'include',
			method: 'POST',
			// no need to set Content-Type header when using FormData
			body: form
		});
	}

	async function register() {
		console.log('register');
		const res = await fetch(`${PUBLIC_BACKEND_URL}/signup`, {
			credentials: 'include',
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				email: username,
				password: password
			})
		});
	}
</script>

<form>
	<input bind:value={username} class="text-black" type="text" placeholder="Username" />
	<input bind:value={password} class="text-black" type="text" placeholder="Password" />
	<button on:click={login} type="submit">Login</button>
	<button on:click={register} type="button">Register</button>
</form>
