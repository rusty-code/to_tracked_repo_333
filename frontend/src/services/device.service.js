import {ApiService} from "@/services/api.service.js";


export const deviceService = {
	list: () => ApiService.get('/devices'),
	get: (id) => ApiService.get(`/devices/${id}`),
	history: (id, minutes = 15) => ApiService.get(`/devices/${id}/history?minutes=${minutes}`),
	create: (device) => ApiService.post('/devices', device),
	update: (id, device) => ApiService.put(`/devices/${id}`, device),
	remove: (id) => ApiService.del(`/devices/${id}`),
	command: (id, command, value = null) => ApiService.post(`/devices/${id}/command`, { command, value }),
	simulate: (id, values) => ApiService.post(`/devices/${id}/simulate`, values),
	setOnline: (id, online) => ApiService.post(`/devices/${id}/online`, { online }),
}

export const scenarioService = {
	list: () => ApiService.get('/scenarios'),
	create: (scenario) => ApiService.post('/scenarios', scenario),
	update: (id, scenario) => ApiService.put(`/scenarios/${id}`, scenario),
	remove: (id) => ApiService.del(`/scenarios/${id}`),
	run: (id) => ApiService.post(`/scenarios/${id}/run`),
}

export const journalService = {
	log: () => ApiService.get('/log'),
	notifications: (to = '') => ApiService.get(`/notifications${to ? '?to=' + to : ''}`),
	reset: () => ApiService.post('/reset'),
}

// значение сигнала для показа: подпись из списка или число с единицей
export function formatValue(signal, value) {
	if (value === undefined || value === null) return '—';
	if (signal?.values && signal.values[String(value)] !== undefined) return signal.values[String(value)];
	return signal?.unit ? `${value} ${signal.unit}` : String(value);
}

// устройство с сервера → формат редактора (DeviceEditor) и обратно
export function toEditor(d) {
	return {
		id: d.id,
		name: d.title,
		room: d.room,
		guid: d.ujin_ext,
		section: d.section,
		type: d.type,
		state: d.state,
		params: d.signals.map((s) => ({
			name: s.name,
			title: s.title,
			type: s.type || (Object.keys(s.values).length ? 'list' : 'number'),
			unit: s.unit,
			values: Object.entries(s.values).map(([k, v]) => `${k}=${v}`).join(';'),
			alarm: s.alarm,
		})),
		events: d.events.map((e) => ({ name: e.name, title: e.title, when: e.when })),
		commands: d.commands.map((c) => ({
			name: c.name,
			title: c.title,
			param: Object.keys(c.set).find((k) => c.set[k] === '$value') ?? '',
			set: c.set,
		})),
		settings: d.settings.map((s) => ({ ...s })),
	}
}

export function fromEditor(dr) {
	const parseValues = (text) => Object.fromEntries(
		(text || '').split(';').map((p) => p.split('=').map((x) => x.trim())).filter(([k, v]) => k !== '' && v)
	);
	return {
		id: dr.id,
		title: dr.name,
		room: dr.room,
		ujin_ext: dr.guid,
		section: dr.section,
		type: dr.type,
		state: dr.state || {},
		signals: dr.params.map((p) => ({
			name: p.name, title: p.title, type: p.type, unit: p.unit,
			values: p.type === 'list' ? parseValues(p.values) : {},
			alarm: p.alarm || '',
		})),
		events: dr.events.map((e) => ({ name: e.name, title: e.title, when: e.when || {} })),
		commands: dr.commands.map((c) => ({
			name: c.name,
			title: c.title,
			set: c.param ? { [c.param]: '$value' } : (c.set && !Object.values(c.set).includes('$value') ? c.set : {}),
		})),
		settings: dr.settings,
	}
}
