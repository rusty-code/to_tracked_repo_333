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
	<aside class="panel list">
		<h2 class="panel__title">Устройства</h2>
		<p class="panel__sub">конструктор, п.1</p>
		
		<ul class="items">
			<li
				v-for="d in devices"
				:key="d.id"
				class="item"
				:class="{ 'item--active': d.id === selectedId }"
				@click="emit('select', d.id)"
			>
				<span class="item__icon">{{ d.icon }}</span>
				<span class="item__body">
          <span class="item__name">{{ d.name }}</span>
          <span class="item__meta">{{ d.room }} · {{ featureCount(d) }} возможностей</span>
        </span>
				<span class="dot" />
			</li>
		</ul>
		
		<h3 class="add__title">Добавить</h3>
		<select v-model="templateKey" class="field">
			<option v-for="t in templates" :key="t.key" :value="t.key">{{ t.icon }} {{ t.title }}</option>
		</select>
		<button type="button" class="btn btn--primary add__btn" @click="emit('create', templateKey)">Создать</button>
	</aside>
</template>

<style scoped>
.list { padding: 14px 12px; align-self: start; }
.panel__title { margin: 0 0 4px 0; font-size: 14px; font-weight: 700; color: #fff; }
.panel__sub { margin: 0 0 12px; font-size: 11px; color: var(--muted); }

.items { list-style: none; margin: 0 0 16px; padding: 0; display: grid; gap: 6px; }
.item {
	display: flex;
	align-items: center;
	gap: 8px;
	padding: 9px 10px;
	border: 1px solid transparent;
	border-radius: 8px;
	cursor: pointer;
}
.item:hover { background: rgba(255, 255, 255, 0.03); }
.item--active { background: var(--accent-bg); border-color: var(--accent-border); }

.item__body { display: flex; flex-direction: column; flex: 1; min-width: 0; }
.item__name { font-size: 12.5px; color: #fff; }
.item__meta { margin-top: 3px; font-size: 10.5px; color: var(--muted); }

.dot { width: 7px; height: 7px; border-radius: 50%; background: var(--green); flex: none; }

.add__title {
	margin: 0 0 8px;
	font-size: 11px;
	letter-spacing: 0.04em;
	text-transform: uppercase;
	color: var(--muted);
}
.add__btn { margin-top: 8px; }
</style>