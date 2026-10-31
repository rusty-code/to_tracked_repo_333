<style scoped>

.devices-view {
	display: grid;
	grid-template-columns: 1fr 5fr;
	height: 100%;
	width: 100%;
}




</style>

<script setup>

// import {useDeviceStore} from "@/stores/device.store.js";
import { computed, onMounted, ref, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';

import PageMenuCard from "@/components/PageMenuCard.vue";
import DeviceAbout from "@/components/DeviceAbout.vue";

// onMounted(() => {
// 	useDeviceStore.fetchDeviceList();
// })


</script>

<template>
	<div class="devices-view">
		<PageMenuCard/>
		<DeviceAbout/>
	</div>
</template>