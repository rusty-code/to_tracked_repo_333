<style scoped>

.button {
	display: block;
	width: 100%;
	padding: 9px 12px;
	border-radius: 6px;
	font-family: var(--font-main);
	font-size: 14px;
	color: var(--text);
	cursor: pointer;
	transition: background-color 0.15s;
}

.button:hover {
	background-color: var(--hover-color);
}

.enabled {
	background-color: var(--accent-light);
	color: var(--accent);
	font-weight: bold;
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
	active: {
		type: Boolean,
		default: false
	},
});

</script>

<template>
	<div
		:id="props.id"
		class="button"
		:class="{ enabled: props.active }"
	>
		{{ props.title }}
	</div>
</template>
