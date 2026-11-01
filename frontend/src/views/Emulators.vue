<script setup>
import { reactive, ref } from 'vue'
import { deviceService, journalService, formatValue } from '@/services/device.service.js'
import { usePolling } from '@/services/poll.js'

const devices = ref([])
const inputs = reactive({})

async function load() {
	devices.value = await deviceService.list()
}

async function simulate(d, s) {
	const raw = inputs[d.id + '.' + s.name]
	if (raw === undefined || raw === '') return
	await deviceService.simulate(d.id, { [s.name]: Number(raw) })
	load()
}

async function toggleOnline(d) {
	await deviceService.setOnline(d.id, !d.online)
	load()
}

async function reset() {
	if (!confirm('Вернуть стартовые устройства и сценарии?')) return
	await journalService.reset()
	load()
}

usePolling(load, 2000)
</script>

<template>
	<div class="page">
		<div class="page-head">
			<h1>Эмуляторы</h1>
			<span class="hint">Задайте показание датчика — сработают события и сценарии, как от настоящего устройства</span>
			<button type="button" style="margin-left: auto" @click="reset">Вернуть стартовые данные</button>
		</div>

		<div class="panel">
			<table>
				<tr>
					<th>Устройство</th>
					<th>Сигнал</th>
					<th>Сейчас</th>
					<th>Новое значение</th>
					<th>На связи</th>
				</tr>
				<template v-for="d in devices" :key="d.id">
					<tr v-for="(s, i) in d.signals" :key="s.name">
						<td v-if="i === 0" :rowspan="d.signals.length"><b>{{ d.title }}</b><br><span class="muted">{{ d.room }}</span></td>
						<td>{{ s.title }}</td>
						<td :class="{ bad: s.alarm && String(d.state[s.name]) === s.alarm }">{{ formatValue(s, d.state[s.name]) }}</td>
						<td>
							<div class="row">
								<select v-if="s.type === 'list'" v-model="inputs[d.id + '.' + s.name]" style="width: 140px">
									<option value="" disabled>выберите</option>
									<option v-for="(label, v) in s.values" :key="v" :value="v">{{ label }}</option>
								</select>
								<input v-else v-model="inputs[d.id + '.' + s.name]" type="number" step="any" placeholder="число" style="width: 140px" />
								<button type="button" @click="simulate(d, s)">Применить</button>
							</div>
						</td>
						<td v-if="i === 0" :rowspan="d.signals.length">
							<label class="row">
								<input type="checkbox" :checked="d.online" @change="toggleOnline(d)" />
								<span :class="d.online ? 'ok' : 'bad'">{{ d.online ? 'да' : 'нет' }}</span>
							</label>
						</td>
					</tr>
				</template>
			</table>
		</div>
	</div>
</template>
