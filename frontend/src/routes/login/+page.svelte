<script lang="ts">
	let username = '';
	let password = '';

	async function login() {
		console.log('login');
		const res = await fetch('https://localhost:8002/login', {
			credentials: 'include',
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				username: username,
				password: password
			})
		});
	}

	async function register() {
		console.log('register');
		const res = await fetch('https://localhost:8002/signup', {
			credentials: 'include',
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				username: username,
				password: password
			})
		});
	}
</script>

<form>
	<input type="text" placeholder="Username" />
	<input type="password" placeholder="Password" />
	<button on:click={login} type="submit">Login</button>
	<button on:click={register} type="button">Register</button>
</form>
