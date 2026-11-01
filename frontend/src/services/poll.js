import { onMounted, onUnmounted } from 'vue'

// вызывать fn сразу и потом каждые ms, пока страница открыта
export function usePolling(fn, ms = 2000) {
	let timer = null;
	onMounted(() => {
		fn();
		timer = setInterval(fn, ms);
	});
	onUnmounted(() => clearInterval(timer));
}
