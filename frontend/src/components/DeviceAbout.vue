
<style scoped>

.device-about-card-body {
	grid-column: 2;
	display: flex;
	flex-direction: column;
	margin-left: 10px;
}

.signal {
	display: flex;
	flex-direction: row;
	height: auto;
	gap: 10px;
	margin-top: 10px;
	
	
}

.signal-param {
	border-radius: var(--border-radius);
	border: 1px solid;
	
	font-size: 1.5rem;
}

</style>

<script setup>

</script>

<template>
	<div class="device-about-card-body">
		<h1>Устройство "Датчик задымления"</h1>
		<h2>Сигналы:</h2>
		<div class="signal">
			<div class="signal-param"> leak-detected </div>
			<div class="signal-param" > Обнаружена протечка </div>
			<div class="signal-param"> X </div>
		</div>
		<div class="signal">
			<div class="signal-param"> +Добавить </div>
		</div>
		
		
		<h2>Команды:</h2>
		<div class="signal">
			<div class="signal-param"> self-test </div>
			<div class="signal-param"> Проверка доступности </div>
			<div class="signal-param"> X </div>
		</div>
		<div class="signal">
			<div class="signal-param"> +Добавить </div>
		</div>
		
	</div>
</template>