<script setup>
import { computed, onMounted, ref } from 'vue'
import DeviceList from '@/components/DeviceList.vue'
import DeviceEditor from '@/components/DeviceEditor.vue'
import { deviceService, toEditor, fromEditor } from '@/services/device.service.js'

defineOptions({ name: 'Devices' })

const devices = ref([])
const selectedId = ref(null)

const selected = computed(() => devices.value.find((d) => d.id === selectedId.value) ?? null)

// шаблон нового устройства — копия существующего или пустое
const deviceTemplates = computed(() => [
	{ key: '', title: 'Пустое устройство' },
	...devices.value.filter((d) => !d.isNew).map((d) => ({ key: d.id, title: 'Как: ' + d.name })),
])

onMounted(async () => {
	devices.value = (await deviceService.list()).map(toEditor)
	selectedId.value = devices.value[0]?.id ?? null
})

function onCreate(templateKey) {
	const base = devices.value.find((d) => d.id === templateKey)
	const id = (base ? base.type || base.id : 'device') + '_' + Date.now().toString().slice(-5)
	const device = base
		? { ...JSON.parse(JSON.stringify(base)), id, name: base.name + ' (копия)', isNew: true }
		: { id, name: 'Новое устройство', room: '', guid: '', section: 'service', type: '', state: {},
			params: [], events: [], commands: [], settings: [], isNew: true }
	devices.value.push(device)
	selectedId.value = device.id
}

async function onSave(updated) {
	try {
		const body = fromEditor(updated)
		const saved = updated.isNew ? await deviceService.create(body) : await deviceService.update(updated.id, body)
		const i = devices.value.findIndex((d) => d.id === updated.id)
		if (i !== -1) devices.value[i] = toEditor(saved)
	} catch (e) {
		alert(e.message)
	}
}

async function onDelete(id) {
	const i = devices.value.findIndex((d) => d.id === id)
	if (i === -1) return
	try {
		if (!devices.value[i].isNew) await deviceService.remove(id)
	} catch (e) {
		return alert(e.message)
	}
	devices.value.splice(i, 1)
	selectedId.value = devices.value[Math.min(i, devices.value.length - 1)]?.id ?? null
}
</script>

<template>
	<div class="page">
		<div class="page-head">
			<h1>Устройства</h1>
			<span class="hint">Что устройство показывает, какие события сообщает и какими командами управляется</span>
		</div>
		<div class="devices">
			<DeviceList
				:devices="devices"
				:selected-id="selectedId"
				:templates="deviceTemplates"
				@select="selectedId = $event"
				@create="onCreate"
			/>
			
			<DeviceEditor v-if="selected" :key="selected.id" :device="selected" @save="onSave" @delete="onDelete" />
			<p v-else class="hint">Выберите устройство слева или создайте новое.</p>
		</div>
	</div>
</template>

<style>
.devices {
	display: flex;
	align-items: flex-start;
	gap: 16px;
}
.devices .panel--list {
	width: 280px;
	flex: none;
}
.devices .panel--editor {
	flex: 1;
	min-width: 0;
}
.devices h2 {
	font-size: 16px;
	margin-bottom: 12px;
}
.devices ul {
	list-style: none;
	padding: 0;
	margin: 0 0 16px;
	display: flex;
	flex-direction: column;
	gap: 4px;
}
.devices .panel--list li button {
	width: 100%;
	height: auto;
	padding: 8px 10px;
	text-align: left;
	border-color: transparent;
}
.devices .panel--list li button:disabled {
	background: var(--accent-light);
	color: var(--accent);
	font-weight: bold;
}
.devices .panel--list select {
	width: 100%;
	margin-bottom: 8px;
}
.devices .panel--editor td {
	padding: 4px 8px 4px 0;
	border: none;
}
.devices .panel--editor th {
	padding: 4px 8px 4px 0;
	border: none;
}
.devices .panel--editor td input,
.devices .panel--editor td select {
	width: 100%;
}
</style>

<style>
.devices .fields {
	display: grid;
	grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
	gap: 12px;
}
.devices .fields label {
	display: flex;
	flex-direction: column;
	gap: 4px;
	color: var(--muted);
	font-size: 13px;
}
.devices .fields input,
.devices .fields select {
	color: var(--text);
}
</style>

<style>
.devices .panel--editor td select {
	min-width: 110px;
}
.devices .panel--editor td input[type="number"] {
	min-width: 80px;
}
</style>
