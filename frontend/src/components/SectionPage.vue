<script setup>
import { ref } from 'vue'
import DeviceCard from '@/components/DeviceCard.vue'
import { deviceService, journalService } from '@/services/device.service.js'
import { usePolling } from '@/services/poll.js'

const props = defineProps({
	section: { type: String, required: true },
	title: { type: String, required: true },
	hint: { type: String, default: '' },
	withHistory: { type: Boolean, default: false },
})

const devices = ref([])
const history = ref({})
const notifications = ref([])

async function load() {
	const all = await deviceService.list()
	devices.value = all.filter((d) => d.section === props.section)
	notifications.value = await journalService.notifications(props.section)
	if (props.withHistory) {
		for (const d of devices.value) history.value[d.id] = await deviceService.history(d.id)
	}
}

usePolling(load, 2000)
</script>

<template>
	<div class="page">
		<div class="page-head">
			<h1>{{ title }}</h1>
			<span class="hint">{{ hint }}</span>
		</div>

		<div class="panel">
			<h3 style="margin: 0 0 8px">Уведомления</h3>
			<p v-if="!notifications.length" class="muted">Новых уведомлений нет</p>
			<table>
				<tr v-for="(n, i) in notifications.slice(0, 5)" :key="i">
					<td class="muted" style="width: 80px">{{ n.time }}</td>
					<td :class="{ bad: i === 0 }">{{ n.text }}</td>
				</tr>
			</table>
		</div>

		<div class="cards">
			<DeviceCard
				v-for="d in devices"
				:key="d.id"
				:device="d"
				:history="withHistory ? history[d.id] || {} : null"
				@changed="load"
			/>
		</div>
	</div>
</template>
