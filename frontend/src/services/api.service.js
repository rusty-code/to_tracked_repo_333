
const API_HOST = 'http://localhost:80/api/';

export const ApiService =
	{
		async run(
			endpoint,
			body = { 'mok': 0 }
		) {
			if (!endpoint) {
				console.error('No endpoint');
				return null;
			}
			
			console.log('Endpoint: ', endpoint);
			
			let headers_data = {
				'Content-Type': 'application/json',
			};
			
			if (sessionStorage.hasOwnProperty('accessToken')) {
				headers_data.Token = sessionStorage.getItem('accessToken');
			}
			
			let init = {
				method: 'POST',
				headers: headers_data
			};
			
			init.body = JSON.stringify(body);
			const response = await fetch(API_HOST + endpoint, init);
			
			if (!response.ok) {
				console.log(await response.text());
				return {};
			}
			
			try {
				console.log('ApiService -> convert');
				const responseJson = await response.json();
				console.log('ApiService -> convert end');
				if (responseJson.status !== 1) {
					console.log(responseJson.data);
					return {};
				}
				console.log(responseJson);
				return responseJson.data;
			}
			catch (error) {
				console.log("Runtime error:");
				console.error(error);
				return {};
			}
		}
	}