<script setup>
import { computed, reactive } from 'vue'
import Sparkline from '@/components/Sparkline.vue'
import { deviceService, formatValue } from '@/services/device.service.js'

const props = defineProps({
	device: { type: Object, required: true },
	history: { type: Object, default: null },
})
const emit = defineEmits(['changed'])

const values = reactive({})

const setting = (name) => props.device.settings.find((s) => s.name === name)?.value

const normText = computed(() => {
	const min = setting('norm_min'), max = setting('norm_max')
	const unit = props.device.signals.find((s) => s.type !== 'list')?.unit || ''
	if (min !== undefined && max !== undefined) return `от ${min} до ${max} ${unit}`.trim()
	if (max !== undefined) return `не больше ${max} ${unit}`.trim()
	if (min !== undefined) return `не меньше ${min} ${unit}`.trim()
	return ''
})

// вне нормы: выше norm_max / ниже norm_min из настроек устройства
function outOfNorm(signal) {
	const v = props.device.state[signal.name]
	if (signal.alarm) return String(v) === signal.alarm
	if (typeof v !== 'number' || signal.type === 'list') return false
	const min = setting('norm_min'), max = setting('norm_max')
	return (min !== undefined && v < min) || (max !== undefined && v > max)
}

function needsValue(cmd) {
	return Object.values(cmd.set).includes('$value')
}

async function run(cmd) {
	try {
		await deviceService.command(props.device.id, cmd.name, needsValue(cmd) ? Number(values[cmd.name]) : null)
		emit('changed')
	} catch (e) {
		alert(e.message)
	}
}
</script>

<template>
	<div class="panel">
		<div class="row" style="justify-content: space-between; margin-bottom: 8px">
			<div>
				<b style="font-size: 15px">{{ device.title }}</b><br>
				<span class="muted">{{ device.room }}</span>
			</div>
			<span :class="device.online ? 'ok' : 'bad'">{{ device.online ? 'на связи' : 'нет связи' }}</span>
		</div>

		<table>
			<tr v-for="s in device.signals" :key="s.name">
				<td>{{ s.title }}</td>
				<td :class="{ bad: outOfNorm(s) }">{{ formatValue(s, device.state[s.name]) }}</td>
			</tr>
		</table>

		<p v-if="normText" class="muted" style="margin-top: 4px">Норма: {{ normText }}</p>

		<template v-if="history">
			<div v-for="s in device.signals.filter((x) => x.type !== 'list')" :key="s.name" style="margin-top: 8px">
				<span class="muted">{{ s.title }} за 15 минут</span><br>
				<Sparkline :points="history[s.name] || []" />
			</div>
		</template>

		<div class="row" style="margin-top: 12px" v-if="device.commands.length">
			<template v-for="c in device.commands" :key="c.name">
				<input v-if="needsValue(c)" v-model="values[c.name]" type="number" placeholder="значение" style="width: 100px" />
				<button type="button" :disabled="!device.online" @click="run(c)">{{ c.title }}</button>
			</template>
		</div>
	</div>
</template>
