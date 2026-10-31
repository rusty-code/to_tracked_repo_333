<script setup>
import { computed, ref } from 'vue'
import DeviceList from '@/components/DeviceList.vue'
import DeviceEditor from '@/components/DeviceEditor.vue'
import { createDevice, deviceTemplates, initialDevices } from './DevicesMock'

defineOptions({ name: 'Devices' })

const devices = ref(initialDevices)
const selectedId = ref(devices.value[0]?.id ?? null)

const selected = computed(() => devices.value.find((d) => d.id === selectedId.value) ?? null)

function onCreate(templateKey) {
	const device = createDevice(templateKey)
	devices.value.push(device)
	selectedId.value = device.id
}

function onSave(updated) {
	const i = devices.value.findIndex((d) => d.id === updated.id)
	if (i !== -1) devices.value[i] = updated
}

function onDelete(id) {
	const i = devices.value.findIndex((d) => d.id === id)
	if (i === -1) return
	devices.value.splice(i, 1)
	selectedId.value = devices.value[Math.min(i, devices.value.length - 1)]?.id ?? null
}
</script>

<template>
	<div class="devices">
		<DeviceList
			:devices="devices"
			:selected-id="selectedId"
			:templates="deviceTemplates"
			@select="selectedId = $event"
			@create="onCreate"
		/>
		
		<DeviceEditor v-if="selected" :key="selected.id" :device="selected" @save="onSave" @delete="onDelete" />
		<p v-else>Выберите устройство или создайте новое.</p>
	</div>
</template>

<style>
.devices {
	--border: 1px solid #444;
	--radius: 8px;
	
	display: flex;
	align-items: flex-start;
	gap: 12px;
	min-height: 100vh;
	padding: 12px;
	//background: #000;
	color: #fff;
	font-family: var(--font-main);
	font-size: 13px;
}
.devices * {
	font-family: var(--font-main);
}
.devices .panel {
	padding: 12px;
	border: var(--border);
	border-radius: var(--radius);
}
.devices .panel--list {
	width: 270px;
	flex: none;
}
.devices .panel--editor {
	flex: 1;
	min-width: 0;
}
.devices input,
.devices select,
.devices button {
	padding: 4px 8px;
	//background: #000;
	//color: #fff;
	border: var(--border);
	border-radius: var(--radius);
	font-size: inherit;
}
.devices button:disabled {
	background: #333;
}
.devices table {
	border-collapse: collapse;
}
.devices th,
.devices td {
	text-align: left;
	padding: 2px 4px;
}
</style>