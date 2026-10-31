import {ApiService} from "@/services/api.service.js";


export const deviceService = {
	async deviceList() {
		return ApiService.run('/api/divices/all')
	}
}