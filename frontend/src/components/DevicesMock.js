// Мок-данные и шаблоны новых устройств (заглушка вместо API)

export const deviceTemplates = [
	{
		key: 'leak',
		icon: '💧',
		title: 'Датчик протечки',
		room: 'Ванная',
		guid: 'ry_leak_01',
		params: [
			{ name: 'leak', title: 'Протечка', type: 'list', unit: '', values: '0=нет;1=протечка' },
			{ name: 'battery', title: 'Батарея', type: 'number', unit: '%', values: '' },
		],
		events: [
			{ name: 'leak_detected', title: 'Обнаружена протечка' },
			{ name: 'leak_cleared', title: 'Протечка устранена' },
		],
		commands: [{ name: 'self_test', title: 'Самотест', param: '' }],
		settings: [
			{ name: 'sensitivity', title: 'Чувствительность', unit: '%', value: 50, min: 0, max: 100 },
		],
	},
	{
		key: 'meter',
		icon: '🚰',
		title: 'Счётчик ХВС с краном',
		room: 'Кухня',
		guid: 'ry_meter_01',
		params: [
			{ name: 'volume', title: 'Объём', type: 'number', unit: 'м³', values: '' },
			{ name: 'valve', title: 'Кран', type: 'list', unit: '', values: '0=закрыт;1=открыт' },
		],
		events: [{ name: 'valve_closed', title: 'Кран закрыт' }],
		commands: [
			{ name: 'open', title: 'Открыть кран', param: '' },
			{ name: 'close', title: 'Закрыть кран', param: '' },
		],
		settings: [{ name: 'pulse_weight', title: 'Вес импульса', unit: 'л', value: 10, min: 1, max: 100 }],
	},
	{
		key: 'light',
		icon: '💡',
		title: 'Свет в прихожей',
		room: 'Прихожая',
		guid: 'ry_light_01',
		params: [
			{ name: 'state', title: 'Состояние', type: 'list', unit: '', values: '0=выкл;1=вкл' },
			{ name: 'brightness', title: 'Яркость', type: 'number', unit: '%', values: '' },
		],
		events: [{ name: 'turned_on', title: 'Свет включён' }],
		commands: [{ name: 'set_brightness', title: 'Задать яркость', param: 'brightness' }],
		settings: [{ name: 'auto_off', title: 'Автоотключение', unit: 'мин', value: 5, min: 0, max: 60 }],
	},
	{
		key: 'thermostat',
		icon: '🌡️',
		title: 'Термостат',
		room: 'Гостиная',
		guid: 'ry_thermo_01',
		params: [{ name: 'temp', title: 'Температура', type: 'number', unit: '°C', values: '' }],
		events: [{ name: 'overheat', title: 'Перегрев' }],
		commands: [{ name: 'set_target', title: 'Целевая температура', param: 'temp' }],
		settings: [{ name: 'hysteresis', title: 'Гистерезис', unit: '°C', value: 1, min: 0, max: 5 }],
	},
	{
		key: 'gate',
		icon: '🚧',
		title: 'Шлагбаум во двор',
		room: 'Двор',
		guid: 'ry_gate_01',
		params: [{ name: 'position', title: 'Положение', type: 'list', unit: '', values: '0=закрыт;1=открыт' }],
		events: [{ name: 'opened', title: 'Открыт' }],
		commands: [{ name: 'open', title: 'Открыть', param: '' }],
		settings: [{ name: 'close_delay', title: 'Задержка закрытия', unit: 'с', value: 30, min: 5, max: 300 }],
	},
]

let seq = 0
const uid = () => `dev_${Date.now()}_${seq++}`

const clone = (v) => JSON.parse(JSON.stringify(v))

/** Создаёт устройство из шаблона */
export function createDevice(templateKey) {
	const t = deviceTemplates.find((x) => x.key === templateKey) ?? deviceTemplates[0]
	return { id: uid(), icon: t.icon, name: t.title, room: t.room, guid: t.guid, ...clone({
			params: t.params, events: t.events, commands: t.commands, settings: t.settings,
		}) }
}

export const initialDevices = deviceTemplates.map((t) => createDevice(t.key))