<script setup>
import MenuButton from "@/components/MenuButton.vue";
</script>
<style scoped>

.card-body {
	user-select: none;
	grid-column: 1;
	display: flex;
	flex-direction: column;
	
	
	border-right: var(--border-style);
	
	margin-left: 5px;
	gap: 10px;
}

.card-body-title {
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	
	width: inherit;
	font-size: 1rem;
	text-align: center;
	padding-top: 10px;
}

.card-body-buttons {
	display: flex;
	flex-direction: column;
	align-items: center;
	gap: 10px;
}

</style>

<script>

import MenuButton from '@/components/MenuButton.vue';

const items = [
	{
		id: "1",
		title: "Датчик протечки"
	},
	{
		id: "1",
		title: "Датчик задымления"
	},
	{
		id: "1",
		title: "Фильтр"
	}
]

</script>

<template>
	<div class="card-body">
		<div class="card-body-title">
			Устройства
		</div>
		
		<div class="card-body-buttons">
			<MenuButton
				v-for="item in items"
				:key="item.id"
				:id="item.id"
				:title="item.title"
			/>
		</div>
		
	</div>
</template>