<script setup>
import { ref, watch } from 'vue'
import SectionTable from './SectionTable.vue'

const props = defineProps({
	device: { type: Object, required: true },
})
const emit = defineEmits(['save', 'delete'])

const clone = (v) => JSON.parse(JSON.stringify(v))

// Работаем с копией, чтобы «Отмена» могла откатить правки
const draft = ref(clone(props.device))
watch(() => props.device, (d) => (draft.value = clone(d)))

const cancel = () => (draft.value = clone(props.device))
const save = () => emit('save', clone(draft.value))

/* ---------- описание таблиц ---------- */
const paramTypes = [
	{ value: 'list', label: 'список' },
	{ value: 'number', label: 'число' },
	{ value: 'text', label: 'текст' },
]

const paramColumns = [
	{ key: 'name', label: 'Имя', kind: 'text', width: '21%' },
	{ key: 'title', label: 'Название', kind: 'text', width: '21%' },
	{ key: 'type', label: 'Тип', kind: 'select', options: paramTypes, width: '10%' },
	{ key: 'unit', label: 'Ед.', kind: 'text', width: '21%' },
	{ key: 'values', label: 'Значения (0=нет;1=да)', kind: 'text', showIf: (r) => r.type === 'list' },
]
const eventColumns = [
	{ key: 'name', label: 'Имя', kind: 'text', width: '50%' },
	{ key: 'title', label: 'Название', kind: 'text' },
]
// Параметр команды — выбор из параметров устройства
const commandColumns = () => [
	{ key: 'name', label: 'Имя', kind: 'text', width: '40%' },
	{ key: 'title', label: 'Название', kind: 'text', width: '40%' },
	{
		key: 'param',
		label: 'Параметр',
		kind: 'select',
		options: [{ value: '', label: 'нет' }, ...draft.value.params.map((p) => ({ value: p.name, label: p.name }))],
	},
]
const settingColumns = [
	{ key: 'name', label: 'Имя', kind: 'text', width: '19%' },
	{ key: 'title', label: 'Название', kind: 'text', width: '19%' },
	{ key: 'unit', label: 'Ед.', kind: 'text', width: '19%' },
	{ key: 'value', label: 'Значение', kind: 'number', width: '19%' },
	{ key: 'min', label: 'Мин', kind: 'number', width: '19%' },
	{ key: 'max', label: 'Макс', kind: 'number' },
]

const newParam = () => ({ name: '', title: '', type: 'number', unit: '', values: '' })
const newEvent = () => ({ name: '', title: '' })
const newCommand = () => ({ name: '', title: '', param: '' })
const newSetting = () => ({ name: '', title: '', unit: '', value: 0, min: 0, max: 100 })
</script>

<template>
	<section class="panel editor">
		<header class="editor__head">
			<h2 class="editor__title">Устройство: {{ device.name }}</h2>
			<span class="badge">тип: {{ device.name }}</span>
		</header>
		
		<div class="row3">
			<label class="label">Название<input v-model="draft.name" class="field" type="text" /></label>
			<label class="label">Помещение<input v-model="draft.room" class="field" type="text" /></label>
			<label class="label">Ujin ext_guid<input v-model="draft.guid" class="field" type="text" /></label>
		</div>
		
		<SectionTable
			v-model="draft.params"
			icon="📊"
			title="Параметры (что измеряет)"
			:columns="paramColumns"
			:create-row="newParam"
		/>
		<SectionTable
			v-model="draft.events"
			icon="⚡"
			title="События (что сообщает)"
			:columns="eventColumns"
			:create-row="newEvent"
		/>
		<SectionTable
			v-model="draft.commands"
			icon="🎛"
			title="Команды (чем управлять)"
			:columns="commandColumns()"
			:create-row="newCommand"
		/>
		<SectionTable
			v-model="draft.settings"
			icon="⚙️"
			title="Настройки (пороги, таймеры)"
			:columns="settingColumns"
			:create-row="newSetting"
		/>
		
		<footer class="actions">
			<button type="button" class="btn btn--primary" @click="save">Сохранить</button>
			<button type="button" class="btn" @click="cancel">Отмена</button>
			<button type="button" class="btn btn--danger" @click="emit('delete', device.id)">Удалить устройство</button>
		</footer>
	</section>
</template>

<style scoped>
.editor { padding: 12px; }
.editor__head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px; }
.editor__title { margin: 0; font-size: 14px; font-weight: 700; color: #fff; }
.badge {
	padding: 2px 8px;
	border-radius: 10px;
	background: rgba(255, 255, 255, 0.06);
	font-size: 10px;
	color: var(--muted);
}

.row3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-bottom: 18px; }
.label { display: flex; flex-direction: column; gap: 4px; font-size: 12px; color: var(--text); }

.actions { display: flex; gap: 8px; margin-top: 6px; }
.actions .btn--danger { margin-left: auto; }
</style>