<script setup>
import { computed, ref } from 'vue'
import DeviceList from './DeviceList.vue'
import DeviceEditor from './DeviceEditor.vue'
import { createDevice, deviceTemplates, initialDevices } from './devicesMock'

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
		
		<DeviceEditor
			v-if="selected"
			:key="selected.id"
			:device="selected"
			@save="onSave"
			@delete="onDelete"
		/>
		<p v-else class="empty">Выберите устройство слева или создайте новое.</p>
	</div>
</template>

<!-- Общие переменные и базовые элементы — без scoped, чтобы работали во всех дочерних компонентах -->
<style>
.devices {
	--bg: #12141a;
	--panel: #1a1d25;
	--field: #1f232d;
	--border: #2b2f3b;
	--text: #d8dae0;
	--muted: #8a8f9c;
	--accent: #8b7cf6;
	--accent-bg: #2a2650;
	--accent-border: #5c52b8;
	--green: #3ecf8e;
	--danger: #ef6a6a;
	
	display: grid;
	grid-template-columns: 270px 1fr;
	gap: 14px;
	align-items: start;
	min-height: 100vh;
	padding: 16px;
	box-sizing: border-box;
	background: var(--bg);
	color: var(--text);
	font: 12px/1.4 ui-monospace, 'JetBrains Mono', 'SF Mono', Menlo, Consolas, monospace;
}
.devices *, .devices *::before, .devices *::after { box-sizing: border-box; }

.devices .panel { background: var(--panel); border: 1px solid var(--border); border-radius: 10px; }

.devices .field {
	width: 100%;
	height: 28px;
	padding: 0 8px;
	border: 1px solid var(--border);
	border-radius: 6px;
	background: var(--field);
	color: var(--text);
	font: inherit;
}
.devices .field:focus { outline: none; border-color: var(--accent); }

.devices .btn {
	height: 28px;
	padding: 0 10px;
	border: 1px solid var(--border);
	border-radius: 6px;
	background: transparent;
	color: var(--text);
	font: inherit;
	cursor: pointer;
}
.devices .btn:hover { border-color: var(--muted); }
.devices .btn--small { height: 22px; padding: 0 8px; margin-top: 6px; font-size: 10.5px; }
.devices .btn--primary { background: var(--accent); border-color: var(--accent); color: #fff; }
.devices .btn--primary:hover { filter: brightness(1.1); border-color: var(--accent); }
.devices .btn--danger { color: var(--danger); border-color: rgba(239, 106, 106, 0.4); }

.devices .empty { padding: 24px; color: var(--muted); }

@media (max-width: 800px) {
	.devices { grid-template-columns: 1fr; }
}
</style>