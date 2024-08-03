import {PUBLIC_API_URL} from '$env/static/public'
import PerformStyleTransferResponse = NSTRequests.PerformStyleTransferResponse;
import StatusResponse = NSTRequests.StatusResponse;

export class NSTService {
	private readonly API_URL: string = PUBLIC_API_URL;
	private static instance: NSTService;

	private constructor() {
	}

	public static getInstance(): NSTService {
		if (!this.instance) {
			this.instance = new NSTService();
		}
		return this.instance;
	}

	public async performStyleTransfer(contentImage: File, styleImage: File): Promise<PerformStyleTransferResponse|null> {
		try {
			const formData: FormData = new FormData();
			formData.append("content_image", contentImage);
			formData.append("style_image", styleImage);

			const response = await fetch(`${PUBLIC_API_URL}/style_transfer`, {
				method: "POST",
				body: formData
			});
			const result = await response.json();
			return result;
		} catch (e) {
			console.log(e);
			return null;
		}
	}

	public async getStatus(taskId: string): Promise<StatusResponse|null> {
		try {
			const response = await fetch(`${PUBLIC_API_URL}/task_status/${taskId}`);
			const result = await response.json();
			return result;
		} catch (e) {
			console.log(e);
			return null;
		}
	}

	public async downloadResultFile(taskId: string): Promise<Blob | null> {
		try {
			const response = await fetch(`${PUBLIC_API_URL}/download/${taskId}`);
			if (!response.ok)
				throw new Error('Network response was not ok');

			return await response.blob();
		} catch (e) {
			console.log(e);
			return null;
		}
	}

	public async downloadAllFiles(taskId: string): Promise<Blob | null> {
		try {
			const response = await fetch(`${PUBLIC_API_URL}/download-all/${taskId}`);
			if (!response.ok)
				throw new Error('Network response was not ok');

			return await response.blob();
		} catch (e) {
			console.log(e);
			return null;
		}
	}

}

export namespace NSTRequests {
	export interface StatusResponse {
		status: string;
		images: string[];
	}

	export interface PerformStyleTransferResponse {
		task_id: string;
	}
}