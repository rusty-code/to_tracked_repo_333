<script setup>
import { ref, watch } from 'vue'
import SectionTable from './SectionTable.vue'

const props = defineProps({
	device: { type: Object, required: true },
})
const emit = defineEmits(['save', 'delete'])

const clone = (v) => JSON.parse(JSON.stringify(v))

const draft = ref(clone(props.device))
watch(() => props.device, (d) => (draft.value = clone(d)))

const cancel = () => (draft.value = clone(props.device))
const save = () => emit('save', clone(draft.value))

const paramTypes = [
	{ value: 'list', label: 'список' },
	{ value: 'number', label: 'число' },
	{ value: 'text', label: 'текст' },
]

const paramColumns = [
	{ key: 'name', label: 'Имя', kind: 'text' },
	{ key: 'title', label: 'Название', kind: 'text' },
	{ key: 'type', label: 'Тип', kind: 'select', options: paramTypes },
	{ key: 'unit', label: 'Ед.', kind: 'text' },
	{ key: 'values', label: 'Значения (0=нет;1=да)', kind: 'text', showIf: (r) => r.type === 'list' },
]
const eventColumns = [
	{ key: 'name', label: 'Имя', kind: 'text' },
	{ key: 'title', label: 'Название', kind: 'text' },
]
const commandColumns = () => [
	{ key: 'name', label: 'Имя', kind: 'text' },
	{ key: 'title', label: 'Название', kind: 'text' },
	{
		key: 'param',
		label: 'Параметр',
		kind: 'select',
		options: [{ value: '', label: 'нет' }, ...draft.value.params.map((p) => ({ value: p.name, label: p.name }))],
	},
]
const settingColumns = [
	{ key: 'name', label: 'Имя', kind: 'text' },
	{ key: 'title', label: 'Название', kind: 'text' },
	{ key: 'unit', label: 'Ед.', kind: 'text' },
	{ key: 'value', label: 'Значение', kind: 'number' },
	{ key: 'min', label: 'Мин', kind: 'number' },
	{ key: 'max', label: 'Макс', kind: 'number' },
]

const newParam = () => ({ name: '', title: '', type: 'number', unit: '', values: '' })
const newEvent = () => ({ name: '', title: '' })
const newCommand = () => ({ name: '', title: '', param: '' })
const newSetting = () => ({ name: '', title: '', unit: '', value: 0, min: 0, max: 100 })
</script>

<template>
	<div class="panel panel--editor">
		<h2>Устройство: {{ device.name }}</h2>
		
		<p>
			<label>Название <input v-model="draft.name" type="text" /></label>
			<label>Помещение <input v-model="draft.room" type="text" /></label>
			<label>ext_guid <input v-model="draft.guid" type="text" /></label>
		</p>
		
		<SectionTable v-model="draft.params" title="Параметры" :columns="paramColumns" :create-row="newParam" />
		<SectionTable v-model="draft.events" title="События" :columns="eventColumns" :create-row="newEvent" />
		<SectionTable v-model="draft.commands" title="Команды" :columns="commandColumns()" :create-row="newCommand" />
		<SectionTable v-model="draft.settings" title="Настройки" :columns="settingColumns" :create-row="newSetting" />
		
		<p>
			<button type="button" @click="save">Сохранить</button>
			<button type="button" @click="cancel">Отмена</button>
			<button type="button" @click="emit('delete', device.id)">Удалить устройство</button>
		</p>
	</div>
</template>