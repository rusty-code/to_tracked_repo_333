<script setup>
import { ref } from 'vue'

defineProps({
	devices: { type: Array, required: true },
	selectedId: { type: String, default: null },
	templates: { type: Array, required: true },
})
const emit = defineEmits(['select', 'create'])

const templateKey = ref('leak')

const featureCount = (d) => d.params.length + d.events.length + d.commands.length + d.settings.length
</script>

<template>
	<div class="panel panel--list">
		<h2>Устройства</h2>
		
		<ul>
			<li v-for="d in devices" :key="d.id">
				<button type="button" :disabled="d.id === selectedId" @click="emit('select', d.id)">
					{{ d.name }} ({{ d.room }}, {{ featureCount(d) }})
				</button>
			</li>
		</ul>
		
		<h3>Добавить</h3>
		<select v-model="templateKey">
			<option v-for="t in templates" :key="t.key" :value="t.key">{{ t.title }}</option>
		</select>
		<button type="button" @click="emit('create', templateKey)">Создать</button>
	</div>
</template>