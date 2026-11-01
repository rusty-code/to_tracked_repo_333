<script setup>
import { computed } from 'vue'

const props = defineProps({
	points: { type: Array, default: () => [] },
	width: { type: Number, default: 240 },
	height: { type: Number, default: 48 },
})

const path = computed(() => {
	const pts = props.points.filter((p) => typeof p[1] === 'number')
	if (pts.length < 2) return ''
	const t0 = pts[0][0], t1 = pts[pts.length - 1][0] || t0 + 1
	const vs = pts.map((p) => p[1])
	let min = Math.min(...vs), max = Math.max(...vs)
	if (min === max) { min -= 1; max += 1 }
	const x = (t) => ((t - t0) / (t1 - t0 || 1)) * (props.width - 4) + 2
	const y = (v) => props.height - 2 - ((v - min) / (max - min)) * (props.height - 4)
	// ступеньками: значение держится до следующего изменения
	let d = `M${x(pts[0][0])},${y(pts[0][1])}`
	for (let i = 1; i < pts.length; i++) d += ` H${x(pts[i][0])} V${y(pts[i][1])}`
	return d
})
</script>

<template>
	<svg v-if="path" :width="width" :height="height" class="sparkline">
		<path :d="path" fill="none" stroke="#00bd7e" stroke-width="1.5" />
	</svg>
	<span v-else class="muted">история копится</span>
</template>
