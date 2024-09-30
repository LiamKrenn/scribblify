<script lang="ts">
	import { BellOff, BellPlus, Check, X } from 'lucide-svelte';
	import { onMount } from 'svelte';

	let isPushSupported = false;
	let pushPermission = 'default';

	onMount(() => {
		isPushSupported = 'PushManager' in window;
		if (isPushSupported) {
			pushPermission = Notification.permission;
			// TODO:
		}
	});

	async function requestPermission() {
		if (!isPushSupported) return;

		try {
			const permission = await Notification.requestPermission();
			pushPermission = permission;
			if (permission === 'granted') {
				subscribeUserToPush();
			}
		} catch (error) {
			console.error('Error requesting permission:', error);
		}
	}

	async function subscribeUserToPush() {
		const registration = await navigator.serviceWorker.ready;
		const subscription = await registration.pushManager.subscribe({
			userVisibleOnly: true,
			applicationServerKey: 'YOUR_PUBLIC_VAPID_KEY' // TODO:
		});

		await sendSubscriptionToServer(subscription);
	}

	async function sendSubscriptionToServer(subscription: PushSubscription) {
		console.log('Sending subscription to server:', subscription);
	}
</script>

{#if isPushSupported}
	{#if pushPermission === 'default'}
		<button
			class="h-12 w-12 rounded-lg bg-slate-700 p-2.5 hover:bg-slate-700/70"
			on:click={requestPermission}
		>
			<BellPlus class="h-full w-full" />
		</button>
	{:else if pushPermission === 'granted'}
		<div class="h-12 w-12 rounded-lg bg-slate-700 p-2.5">
			<Check class="h-full w-full" />
		</div>
	{:else}
		<div class="h-12 w-12 rounded-lg bg-slate-700 p-2.5">
			<BellOff class="h-full w-full" />
		</div>
	{/if}
{:else}
	<div class="h-12 w-12 rounded-lg bg-slate-700 p-2.5">
		<X class="h-full w-full" />
	</div>
{/if}
