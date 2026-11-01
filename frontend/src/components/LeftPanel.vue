<style scoped>

.left-panel {
	user-select: none;
	display: flex;
	flex-direction: column;
	gap: 24px;
	height: 100vh;
	padding: 24px 16px;
	background: var(--color-main);
	border-right: var(--border-style);
	font-family: var(--font-main);
}

.left-panel-title {
	font-size: 18px;
	font-weight: bold;
	padding: 0 12px;
}

.left-panel-title span {
	display: block;
	font-size: 12px;
	font-weight: normal;
	color: var(--muted);
	margin-top: 2px;
}

.group-title {
	font-size: 12px;
	color: var(--muted);
	padding: 0 12px 6px;
}

.page-buttons {
	display: flex;
	flex-direction: column;
	gap: 2px;
}

</style>

<script setup>

import {useRoute, useRouter} from 'vue-router';

import MenuButton from '@/components/MenuButton.vue';

const groups = [
	{
		title: 'Рабочие окна',
		items: [
			{ id: 'service', title: 'Служебное', route: '/service' },
			{ id: 'vet', title: 'Ветеринары', route: '/vet' },
		],
	},
	{
		title: 'Настройка системы',
		items: [
			{ id: 'main-page', title: 'Устройства', route: '/devices' },
			{ id: 'projects', title: 'Сценарии', route: '/scripts' },
			{ id: 'emulators', title: 'Эмуляторы', route: '/emulators' },
			{ id: 'team', title: 'Журнал', route: '/journal' },
		],
	},
]

const router = useRouter();
const route = useRoute();

</script>

<template>
	<aside class="left-panel">
		<div class="left-panel-title">
			Океанариум
			<span>система сценариев</span>
		</div>

		<div v-for="g in groups" :key="g.title">
			<div class="group-title">{{ g.title }}</div>
			<div class="page-buttons">
				<MenuButton
					v-for="item in g.items"
					:key="item.id"
					:id="item.id"
					:title="item.title"
					:active="route.path === item.route"
					@click="router.push(item.route)"
				/>
			</div>
		</div>
	</aside>
</template>
