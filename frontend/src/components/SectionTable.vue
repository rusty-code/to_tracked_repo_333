<script setup>
// Универсальная редактируемая таблица для секций: параметры, события, команды, настройки.
// columns: [{ key, label, kind: 'text'|'number'|'select', options?, width?, showIf? }]
const props = defineProps({
	icon: { type: String, default: '' },
	title: { type: String, required: true },
	columns: { type: Array, required: true },
	createRow: { type: Function, required: true },
})

const rows = defineModel({ type: Array, required: true })

const add = () => rows.value.push(props.createRow())
const remove = (i) => rows.value.splice(i, 1)
</script>

<template>
	<section class="section">
		<h3 class="section__title">
			<span class="section__icon">{{ icon }}</span>{{ title }}
		</h3>
		
		<table class="grid">
			<thead>
			<tr>
				<th v-for="col in columns" :key="col.key" :style="{ width: col.width }">{{ col.label }}</th>
				<th class="grid__del" />
			</tr>
			</thead>
			<tbody>
			<tr v-for="(row, i) in rows" :key="i">
				<td v-for="col in columns" :key="col.key">
					<span v-if="col.showIf && !col.showIf(row)" class="dash">—</span>
					
					<select v-else-if="col.kind === 'select'" v-model="row[col.key]" class="field">
						<option v-for="o in col.options" :key="o.value" :value="o.value">{{ o.label }}</option>
					</select>
					
					<input v-else-if="col.kind === 'number'" v-model.number="row[col.key]" type="number" class="field" />
					
					<input v-else v-model="row[col.key]" type="text" class="field" />
				</td>
				<td class="grid__del">
					<button type="button" class="btn-del" title="Удалить" @click="remove(i)">✕</button>
				</td>
			</tr>
			</tbody>
		</table>
		
		<button type="button" class="btn btn--small" @click="add">+ добавить</button>
	</section>
</template>

<style scoped>
.section { margin-bottom: 16px; }
.section__title {
	margin: 0 0 8px;
	font-size: 12px;
	letter-spacing: 0.04em;
	text-transform: uppercase;
	color: var(--muted);
}
.section__icon { margin-right: 6px; }

.grid { width: 100%; border-collapse: collapse; table-layout: fixed; }
.grid th {
	padding: 4px 5px 6px;
	text-align: left;
	font-size: 10px;
	font-weight: 700;
	letter-spacing: 0.04em;
	text-transform: uppercase;
	color: var(--muted);
}
.grid td { padding: 5px; border-top: 1px solid var(--border); vertical-align: middle; }
.grid__del { width: 36px; }
.dash { color: var(--muted); padding-left: 4px; }

.btn-del {
	width: 24px;
	height: 24px;
	border: 1px solid var(--border);
	border-radius: 5px;
	background: transparent;
	color: var(--danger);
	font-size: 11px;
	cursor: pointer;
}
.btn-del:hover { background: rgba(239, 106, 106, 0.12); }
</style>