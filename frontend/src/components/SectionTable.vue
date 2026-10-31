<script setup>
const props = defineProps({
	title: { type: String, required: true },
	columns: { type: Array, required: true },
	createRow: { type: Function, required: true },
})

const rows = defineModel({ type: Array, required: true })

const add = () => rows.value.push(props.createRow())
const remove = (i) => rows.value.splice(i, 1)
</script>

<template>
	<div>
		<h3>{{ title }}</h3>
		<table>
			<thead>
			<tr>
				<th v-for="col in columns" :key="col.key">{{ col.label }}</th>
				<th></th>
			</tr>
			</thead>
			<tbody>
			<tr v-for="(row, i) in rows" :key="i">
				<td v-for="col in columns" :key="col.key">
					<span v-if="col.showIf && !col.showIf(row)">-</span>
					<select v-else-if="col.kind === 'select'" v-model="row[col.key]">
						<option v-for="o in col.options" :key="o.value" :value="o.value">{{ o.label }}</option>
					</select>
					<input v-else-if="col.kind === 'number'" v-model.number="row[col.key]" type="number" />
					<input v-else v-model="row[col.key]" type="text" />
				</td>
				<td><button type="button" @click="remove(i)">x</button></td>
			</tr>
			</tbody>
		</table>
		<button type="button" @click="add">+ добавить</button>
	</div>
</template>