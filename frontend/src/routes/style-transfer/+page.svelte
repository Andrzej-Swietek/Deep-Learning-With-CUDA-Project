<script lang="ts">
	import { onDestroy, onMount } from 'svelte';
	import PollWorker from './statusPoll.worker.ts?worker'
	import { NSTService } from '@services/NST.service';
	import type { NSTRequests } from '@services/NST.service';
	import PerformStyleTransferResponse = NSTRequests.PerformStyleTransferResponse;

  const POLLING_INTERVAL = 5000; // in ms

	let contentImage: File | null = null;
	let styleImage: File | null = null;
	let status: string = "Idle";
	let resultImages: string[] = [];
	let taskId: string | null = null;

	let contentImageUrl: string | null = null;
	let styleImageUrl: string | null = null;

	let pollingWorker: Worker;

	const handleFileChange = (event: Event, type: 'content' | 'style'): void => {
		const target = event.target as HTMLInputElement;
		const file = target.files[0];
		if (target.files && target.files.length > 0) {
			if (type === 'content') {
				contentImage = target.files[0];
				contentImageUrl = URL.createObjectURL(file);
			} else if (type === 'style') {
				styleImage = target.files[0];
				styleImageUrl = URL.createObjectURL(file);
			}
		}
	}

	const handleDrop = (event: DragEvent, type: string): void => {
		if (event.dataTransfer && event.dataTransfer.files.length > 0) {
			const file = event.dataTransfer.files[0];
			if (type === 'content') {
				contentImage = file;
				contentImageUrl = URL.createObjectURL(file);
			} else if (type === 'style') {
				styleImage = file;
				styleImageUrl = URL.createObjectURL(file);
			}
		}
	}


	const handleWorkerMessage = (event: MessageEvent): void => {
		const { status: workerStatus, images } = event.data;
		if (workerStatus === "Completed") {
			resultImages = images;
			status = "Completed";
			pollingWorker?.terminate();
			pollingWorker = null;
		}
	};

	const uploadImages = async (): Promise<void> => {
		if (!contentImage || !styleImage) {
			alert('Provide both images');
			return;
		}

		const result: NSTRequests.PerformStyleTransferResponse | null
			= await NSTService.getInstance().performStyleTransfer(
					contentImage, styleImage
			);

		if (!result || !result.task_id) {
			alert('Unable to perform action. Try Later');
			return;
		}

		taskId = result.task_id;
		status = "Processing...";

		// Start polling for the task status
		if (!window.Worker) {
			pollTaskStatus(taskId);
		} else {
			pollingWorker.postMessage({ taskId: taskId });
		}

	}

	const pollTaskStatus = async (taskId: string): Promise<void> => {
		const interval = setInterval(async () => {
			const result = await NSTService.getInstance().getStatus(taskId);

			if (result.status === "Completed") {
				clearInterval(interval);
				resultImages = result.images;
				status = "Completed";
			}
		}, POLLING_INTERVAL);
	}

	const downloadOneFile = async () => {
		const result = await NSTService
														.getInstance()
														.downloadResultFile(taskId);
	}

	const downloadAllFile = async () => {
		const result = await NSTService
														.getInstance()
														.downloadAllFiles(taskId);
	}

	onMount(()=>{
		pollingWorker = new PollWorker
		pollingWorker.onmessage = (event: MessageEvent) => {
			handleWorkerMessage(event);
		}
	});

	onDestroy(()=>{
		pollingWorker?.terminate();
		pollingWorker = null;
	})
</script>

<svelte:head>
	<title>Neural Style Transfer</title>
	<meta name="description" content="Neural Style Transfer" />
</svelte:head>

<section class="w-full h-full py-12 md:py-24 lg:py-32 bg-muted flex justify-center items-center">
	<div class="container px-4 md:px-6 grid gap-6 w-full h-[90dvh]">
		<div class="flex flex-col items-center justify-center space-y-4">
			<div class="space-y-2 mb-16">
				<h1 class="text-3xl font-bold tracking-tighter sm:text-5xl xl:text-6xl/none">Neural Style Transfer</h1>
				<p class="max-w-[900px] text-muted-foreground md:text-xl">Seamlessly blend the content of one image with the style of another, creating stunning and unique artworks.</p>
				<p class="max-w-[900px] text-muted-foreground md:text-xl font-bold">Status: {status}</p>
				{#if status === 'Completed' || status === 'Finished'}
					<div class="w-full flex flex-row justify-center items-center gap-x-8">
						<button
							on:click={() => downloadOneFile()}
							type="button"
							class="inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 h-10 px-32 py-2 mt-16"
						>
							Download File
						</button>
						<button
							on:click={() => downloadAllFile()}
							type="button"
							class="inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 h-10 px-32 py-2 mt-16"
						>
							Download Zip
						</button>
					</div>
				{/if}
			</div>
			<div class="grid grid-cols-2 gap-4 w-full max-w-4xl">
				<div
					on:dragover|preventDefault
					on:drop|preventDefault={(e) => handleDrop(e, 'content')}
					class="flex flex-col items-center justify-center border-2 border-dashed border-black rounded-lg p-24 space-y-2">
					<svg
						xmlns="http://www.w3.org/2000/svg"
						width="24"
						height="24"
						viewBox="0 0 24 24"
						fill="none"
						stroke="currentColor"
						stroke-width="2"
						stroke-linecap="round"
						stroke-linejoin="round"
						class="w-8 h-8 text-muted-foreground"
					>
						<rect width="18" height="18" x="3" y="3" rx="2" ry="2"></rect>
						<circle cx="9" cy="9" r="2"></circle>
						<path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"></path>
					</svg>
					<p class="text-sm text-muted-foreground">Upload Content Image</p>
					<input
						class="flex h-10 rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 w-full"
						placeholder="Upload content image"
						accept="image/png, image/jpeg"
						type="file"
						bind:value={contentImage}
						on:change="{(e) => handleFileChange(e, 'content')}"
					/>
				</div>
				<div
						on:dragover|preventDefault
						on:drop|preventDefault={(e) => handleDrop(e, 'style')}
						class="flex flex-col items-center justify-center border-2 border-dashed border-black rounded-lg p-24 space-y-2"
				>
					<svg
						xmlns="http://www.w3.org/2000/svg"
						width="24"
						height="24"
						viewBox="0 0 24 24"
						fill="none"
						stroke="currentColor"
						stroke-width="2"
						stroke-linecap="round"
						stroke-linejoin="round"
						class="w-8 h-8 text-muted-foreground"
					>
						<rect width="18" height="18" x="3" y="3" rx="2" ry="2"></rect>
						<circle cx="9" cy="9" r="2"></circle>
						<path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"></path>
					</svg>
					<p class="text-sm text-muted-foreground">Upload Style Image</p>
					<input
						class="flex h-10 rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 w-full"
						placeholder="Upload style image"
						accept="image/png, image/jpeg"
						type="file"
						bind:value={styleImage}
						on:change="{(e) => handleFileChange(e, 'style')}"
					/>
				</div>
				{#if contentImage}
					<div class="flex flex-col items-center justify-center gap-4">
						<p class="text-muted-foreground md:text-xl">Content image preview:</p>
						<img class="w-[300px] h-[300px] object-cover rounded-md"  src={contentImageUrl} alt="preview contnent">
					</div>
				{/if}
				{#if styleImage}
					<div class="flex flex-col items-center justify-center gap-4">
						<p class="text-muted-foreground md:text-xl">Style image preview:</p>
						<img class="w-[300px] h-[300px] object-cover rounded-md" src={styleImageUrl} alt="preview contnent">
					</div>
				{/if}
			</div>
			<button
				class="inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 h-10 px-32 py-2 mt-16"
				type="button"
				on:click={uploadImages}
			>
				Transfer
			</button>
		</div>
		<div class="mt-8">
			{#if resultImages.length > 0}
				<h2 class="text-2xl font-bold mt-4">Results</h2>
				<div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
					{#each resultImages as image}
						<img src={image} alt="Stylized Image" class="w-full h-auto" />
					{/each}
				</div>
			{/if}
		</div>
	</div>
</section>

