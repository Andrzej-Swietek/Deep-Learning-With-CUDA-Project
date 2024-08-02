onmessage = async (event) => {
	const { taskId } = event.data;
	const POLLING_INTERVAL = 5000; // in ms

	const pollTaskStatus = async (): Promise<void> => {
		const interval = setInterval(async (): Promise<void> => {
			const response = await fetch(`http://0.0.0.0:5000/api/task_status/${taskId}`);
			const result = await response.json();

			if (result.status === "Completed") {
				clearInterval(interval);
				postMessage({
					status: "Completed",
					images: result.images
				});
			}
		}, POLLING_INTERVAL); // Check every 5 seconds
	};

	await pollTaskStatus();
};

export {}