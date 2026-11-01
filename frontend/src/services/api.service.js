
const API_HOST = '/api';

export const ApiService =
	{
		async request(method, endpoint, body) {
			let init = { method, headers: {} };

			if (body !== undefined) {
				init.headers['Content-Type'] = 'application/json';
				init.body = JSON.stringify(body);
			}

			const response = await fetch(API_HOST + endpoint, init);
			const data = await response.json().catch(() => null);

			if (!response.ok) {
				const detail = data?.detail;
				throw new Error(Array.isArray(detail) ? detail.join('\n') : detail || response.statusText);
			}
			return data;
		},

		get: (endpoint) => ApiService.request('GET', endpoint),
		post: (endpoint, body = {}) => ApiService.request('POST', endpoint, body),
		put: (endpoint, body) => ApiService.request('PUT', endpoint, body),
		del: (endpoint) => ApiService.request('DELETE', endpoint),
	}
