<script setup>
import { ref } from 'vue'
import { journalService } from '@/services/device.service.js'
import { usePolling } from '@/services/poll.js'

const log = ref([])
const notifications = ref([])
const who = { service: 'служебное', vet: 'ветеринары' }

usePolling(async () => {
	log.value = await journalService.log()
	notifications.value = await journalService.notifications()
}, 2000)
</script>

<template>
	<div class="page">
		<div class="page-head">
			<h1>Журнал</h1>
			<span class="hint">События устройств, запуски сценариев, команды и уведомления</span>
		</div>
		<div class="cards" style="grid-template-columns: 1fr 1fr">
			<div class="panel">
				<h3 style="margin: 0 0 8px">События и действия</h3>
				<table>
					<tr v-for="(l, i) in log" :key="i">
						<td class="muted" style="width: 80px">{{ l.time }}</td>
						<td>{{ l.text }}</td>
					</tr>
				</table>
				<p v-if="!log.length" class="muted">Пусто</p>
			</div>
			<div class="panel">
				<h3 style="margin: 0 0 8px">Уведомления</h3>
				<table>
					<tr v-for="(n, i) in notifications" :key="i">
						<td class="muted" style="width: 80px">{{ n.time }}</td>
						<td>{{ who[n.to] || n.to }}</td>
						<td>{{ n.text }}</td>
					</tr>
				</table>
				<p v-if="!notifications.length" class="muted">Пусто</p>
			</div>
		</div>
	</div>
</template>
