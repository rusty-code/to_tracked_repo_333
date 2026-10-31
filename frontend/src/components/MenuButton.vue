<style scoped>

.button {
	display: grid;
	grid-template-columns: 1fr 1fr 2fr;
	align-items: center;
	text-align: center;
	gap: 20px;
	padding-left: 20px;
	
	width: 90%;
	max-width: 90%;
	height: 45px;

	transition: background-color 0.15s;
	
	
	border: var(--border-style);
	border-radius: var(--border-radius);
	
	cursor: pointer;
}

.button:hover {
	background-color: var(--hover-color);
	cursor: pointer;
}

.button .logo {
	grid-column: 1;
	margin-left: auto;
	width: 30px;
	background-color: rgba(255, 255, 255, 0);
}

.button .text {
	grid-column: 2;
	font-size: 100%;
	margin-left: auto;
	background-color: rgba(255, 255, 255, 0);
	font-family: var(--font-main);
}

.enabled {
	background-color: rgba(255, 255, 255, 0.75);
}

</style>

<script setup>

const props = defineProps({
	id: {
		type: String,
		required: true
	},
	title: {
		type: String,
		required: true
	},
});



</script>

<template>
	<div
		:id="props.id"
		class="button"
	>
		<img
			:src="props.icon"
			class="logo"
			alt="ERR"/>
		<span
			class="text"
		> {{props.title}} </span>
	</div>
</template>