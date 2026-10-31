<style scoped>

.left-panel {
	user-select: none;
	
	grid-column: 1;
	position: relative;
	
	display: flex;
	flex-direction: column;
	
	align-self: center;
	justify-self: center;
	
	align-items: center;
	
	height: var(--height-app);
	width: 200px;
	
	border-right: var(--border-style);
	
	margin-left: 10px;
	
	gap: 20px;
}

.left-panel-title {
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: center;
	
	width: inherit;
	max-width: 200px;
	
	font-size: 1.5rem;
	
	text-align: center;
	padding-top: 20px;
}

.left-panel-title-img {
	width: 30%;
}

.left-menu-bar {
	display: flex;
	flex-direction: column;
	
	justify-content: space-between;
	align-self: center;
	align-items: center;
	
	width: 100%;
	height: 85%;
}

.page-buttons {
	display: flex;
	flex-direction: column;
	
	align-items: center;
	
	gap: 10px;
}

</style>

<script setup>

import {useRouter} from 'vue-router';


import MenuButton from '@/components/MenuButton.vue';

// import projectWikiLogo from '@/assets/logo/open-book.svg';
// import homePageLogo from '@/assets/logo/home.svg';
// import projectsPageLogo from '@/assets/logo/folder.svg';
// import teamPageLogo from '@/assets/logo/team.svg';
// import logoutLogo from '@/assets/logo/start.svg'


const items = [
	{
		id: 'main-page',
		title: 'Устройства',
		// icon: homePageLogo,
		route: '/devices'
	},
	{
		id: 'projects',
		title: 'Сценарии',
		// icon: projectsPageLogo,
		route: '/scripts'
	},
	{
		id: 'team',
		title: 'Журнал',
		// icon: teamPageLogo,
		route: '/journal'
	}
]

const router = useRouter();

</script>

<template>
	<aside class="left-panel">
		<div
			class="left-panel-title bold"
		>
			<img
				class="left-panel-title-img"
				alt="ERR"/>
			<span> Smart Ocean </span>
		</div>
		
		<div class="left-menu-bar">
			<div class="page-buttons">
				<MenuButton
					v-for="item in items"
					:key="item.id"
					:id="item.id"
					:title="item.title"
					@click="router.push(item.route)"
				/>
			</div>
		</div>
	</aside>
</template>