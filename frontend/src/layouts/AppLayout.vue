<style scoped>

.main-app {
	display: grid;
	grid-template-columns: 220px 1fr;
	height: 100vh;
	width: 100%;
}

.work-area {
	height: 100vh;
	overflow-y: auto;
}

.page-view {
	max-width: 1280px;
	padding: 24px 32px 40px;
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
