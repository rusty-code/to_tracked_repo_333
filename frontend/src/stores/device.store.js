import defineStore from 'pinia'
import {deviceService} from "@/services/device.service.js";


export const useDeviceStore = defineStore(
	'devices',
	{
		state: () => ({
			deviceList: [],
			selectedDevice: 0,
		}),
		actions: {
			async fetchDeviceList() {
				let devices = await deviceService.deviceList();
				if (devices.length === 0) {
					console.log('deviceStore::fetchDeviceList -> empty');
					return;
				}
				
				console.log('deviceStore::fetchDeviceList -> success');
				this.deviceList = [];
				var counter = 0;
				for (let device of devices.list) {
					this.deviceList.push(device);
					++counter;
				}
			}
		}
	},
);