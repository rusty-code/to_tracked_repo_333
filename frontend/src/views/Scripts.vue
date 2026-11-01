<script setup>
import { computed, onMounted, ref } from 'vue'
import { deviceService, scenarioService } from '@/services/device.service.js'

const scenarios = ref([])
const devices = ref([])
const draft = ref(null)
const error = ref('')

const ops = ['==', '!=', '>', '<', '>=', '<=']
const results = { ok: 'выполнен', skipped: 'пропущен', error: 'с ошибкой' }
const clone = (v) => JSON.parse(JSON.stringify(v))
const dev = (id) => devices.value.find((d) => d.id === id)
const isNew = computed(() => draft.value && !scenarios.value.some((s) => s.id === draft.value.id))

async function load() {
	devices.value = await deviceService.list()
	scenarios.value = await scenarioService.list()
}
onMounted(load)

function select(s) {
	draft.value = clone(s)
	error.value = ''
}

function create() {
	const d = devices.value.find((x) => x.events.length) || devices.value[0]
	draft.value = {
		id: '', title: 'Новый сценарий', enabled: true,
		when: { type: 'event', device: d.id, event: d.events[0]?.name || '', signal: '', op: '==', value: 0 },
		if: [],
		then: [{ type: 'notify', to: 'service', text: '' }],
	}
	error.value = ''
}

// при смене устройства подставляем его первое событие/сигнал/команду
function fixWhen() {
	const w = draft.value.when, d = dev(w.device)
	if (!d) return
	if (!d.events.some((e) => e.name === w.event)) w.event = d.events[0]?.name || ''
	if (!d.signals.some((s) => s.name === w.signal)) w.signal = d.signals[0]?.name || ''
}
function fixIf(c) {
	const d = dev(c.device)
	if (d && !d.signals.some((s) => s.name === c.signal)) c.signal = d.signals[0]?.name || ''
}
function fixThen(a) {
	const d = dev(a.device)
	if (d && !d.commands.some((c) => c.name === a.command)) a.command = d.commands[0]?.name || ''
}
const needsValue = (a) => Object.values(dev(a.device)?.commands.find((c) => c.name === a.command)?.set || {}).includes('$value')

function addIf() {
	const d = devices.value[0]
	draft.value.if.push({ device: d.id, signal: d.signals[0]?.name, op: '==', value: 0 })
}
function addThen() {
	const d = devices.value.find((x) => x.commands.length)
	draft.value.then.push({ type: 'command', device: d.id, command: d.commands[0].name, value: null, to: 'service', text: '' })
}

async function save() {
	try {
		const saved = isNew.value ? await scenarioService.create(draft.value) : await scenarioService.update(draft.value.id, draft.value)
		await load()
		select(saved)
	} catch (e) {
		error.value = e.message
	}
}

async function run() {
	await save()
	if (error.value) return
	draft.value = clone(await scenarioService.run(draft.value.id))
	await load()
}

async function remove() {
	if (!confirm('Удалить сценарий?')) return
	if (!isNew.value) await scenarioService.remove(draft.value.id)
	draft.value = null
	load()
}

async function toggle(s) {
	await scenarioService.update(s.id, { ...s, enabled: !s.enabled })
	load()
}
</script>

<template>
	<div class="page">
		<div class="page-head">
			<h1>Сценарии</h1>
			<span class="hint">Когда что-то произошло и выполнены условия — сделать действия по порядку</span>
			<button type="button" class="primary" style="margin-left: auto" @click="create">Новый сценарий</button>
		</div>

		<div class="cards" style="grid-template-columns: 300px minmax(0, 1fr)">
			<div class="panel">
				<table>
					<tr><th style="width: 1%">Вкл.</th><th>Сценарий</th></tr>
					<tr v-for="s in scenarios" :key="s.id">
						<td><input type="checkbox" :checked="s.enabled" @change="toggle(s)" /></td>
						<td style="cursor: pointer" @click="select(s)">
							<b v-if="draft && draft.id === s.id">{{ s.title }}</b>
							<span v-else>{{ s.title }}</span>
							<br><span class="muted">{{ s.last_run ? s.last_run + ' · ' + results[s.last_result] : 'не запускался' }}</span>
						</td>
					</tr>
				</table>
			</div>

			<div class="panel" v-if="draft">
				<div class="row">
					<input v-model="draft.title" placeholder="Название сценария" style="flex: 1; font-weight: bold" />
					<label><input type="checkbox" v-model="draft.enabled" /> включён</label>
				</div>

				<h3>Когда <span class="muted">— что запускает сценарий</span></h3>
				<div class="row">
					<select v-model="draft.when.type">
						<option value="event">событие устройства</option>
						<option value="signal">значение сигнала</option>
						<option value="manual">вручную</option>
					</select>
					<template v-if="draft.when.type !== 'manual'">
						<select v-model="draft.when.device" @change="fixWhen">
							<option v-for="d in devices" :key="d.id" :value="d.id">{{ d.title }}</option>
						</select>
						<select v-if="draft.when.type === 'event'" v-model="draft.when.event">
							<option v-for="e in dev(draft.when.device)?.events" :key="e.name" :value="e.name">{{ e.title }}</option>
						</select>
						<template v-else>
							<select v-model="draft.when.signal">
								<option v-for="s in dev(draft.when.device)?.signals" :key="s.name" :value="s.name">{{ s.title }}</option>
							</select>
							<select v-model="draft.when.op"><option v-for="o in ops" :key="o">{{ o }}</option></select>
							<input v-model.number="draft.when.value" type="number" step="any" style="width: 80px" />
						</template>
					</template>
				</div>

				<h3>Если <span class="muted">— дополнительные условия, необязательно</span></h3>
				<div class="row" v-for="(c, i) in draft.if" :key="i">
					<select v-model="c.device" @change="fixIf(c)">
						<option v-for="d in devices" :key="d.id" :value="d.id">{{ d.title }}</option>
					</select>
					<select v-model="c.signal">
						<option v-for="s in dev(c.device)?.signals" :key="s.name" :value="s.name">{{ s.title }}</option>
					</select>
					<select v-model="c.op"><option v-for="o in ops" :key="o">{{ o }}</option></select>
					<input v-model.number="c.value" type="number" step="any" style="width: 80px" />
					<button type="button" class="danger" style="margin-left: auto" @click="draft.if.splice(i, 1)">Удалить</button>
				</div>
				<p v-if="!draft.if.length" class="muted">Без условий — сценарий выполняется всегда</p>
				<button type="button" style="margin-top: 8px" @click="addIf">Добавить условие</button>

				<h3>То <span class="muted">— что сделать, по порядку</span></h3>
				<div class="row" v-for="(a, i) in draft.then" :key="i">
					<span class="muted">{{ i + 1 }}.</span>
					<select v-model="a.type">
						<option value="command">команда</option>
						<option value="notify">уведомление</option>
					</select>
					<template v-if="a.type === 'command'">
						<select v-model="a.device" @change="fixThen(a)">
							<option v-for="d in devices.filter((x) => x.commands.length)" :key="d.id" :value="d.id">{{ d.title }}</option>
						</select>
						<select v-model="a.command">
							<option v-for="c in dev(a.device)?.commands" :key="c.name" :value="c.name">{{ c.title }}</option>
						</select>
						<input v-if="needsValue(a)" v-model.number="a.value" type="number" step="any" style="width: 80px" />
					</template>
					<template v-else>
						<select v-model="a.to">
							<option value="service">служебное</option>
							<option value="vet">ветеринары</option>
						</select>
						<input v-model="a.text" placeholder="текст уведомления" style="flex: 1; min-width: 200px" />
					</template>
					<button type="button" class="danger" style="margin-left: auto" @click="draft.then.splice(i, 1)">Удалить</button>
				</div>
				<button type="button" style="margin-top: 8px" @click="addThen">Добавить действие</button>

				<pre v-if="error" class="bad">{{ error }}</pre>
				<div class="row" style="margin-top: 24px">
					<button type="button" class="primary" @click="save">Сохранить</button>
					<button type="button" @click="run">Сохранить и запустить</button>
					<button type="button" class="danger" @click="remove">Удалить сценарий</button>
					<span v-if="draft.last_run" class="muted">последний запуск {{ draft.last_run }} · {{ results[draft.last_result] }}</span>
				</div>
			</div>
			<p v-else class="hint">Выберите сценарий слева или создайте новый.</p>
		</div>
	</div>
</template>
