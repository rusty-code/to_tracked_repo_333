<style scoped>

.main-app {
	display: flex;
	flex-direction: row;
	height: 100%;
	width: 100%;
	
	max-height: 100vh;
	max-width: 100vw;
	gap: 15px;
	align-items: center;
}

.work-area {
	width: 100%;
	display: flex;
	flex-direction: column;
	height: var(--height-app);
	margin-right: 20px;
}

.page-view {
	width: 100%;
	height: 100%;
	margin-top: 20px;
	//background-color: var(--color-main);
}

</style>

<script setup>
	import LeftPanel from '@/components/LeftPanel.vue'
</script>

<template>
	<div class="main-app">
		<LeftPanel/>
		<div class="work-area">
			<div class="page-view">
				<router-view/>
			</div>
		</div>
	</div>
</template>