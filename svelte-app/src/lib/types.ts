export type Image = {
	job_id: string;
	image: string | undefined;
	status: string;
	name: string;
	size: number;
	type: string;
	upload_time?: number;
};
