# Связка

Система управления умным океанариумом на Ujin OS: датчики и сценарии «когда — если — то».
Что делаем и какие сценарии — в [Проект.md](Проект.md).

| id | Устройство | Окно | Сигналы | Команды |
|---|---|---|---|---|
| `leak` | Датчик протечки | служебное | `leak`, `water` | `water_off`, `water_on` |
| `light` | Датчик света | служебное | `level` | `set_level` |
| `ventilation` | Датчик вентиляции | служебное | `humidity`, `fan` | `fan_on`, `fan_off` |
| `clock` | Время суток | служебное | `period` (0 день, 1 вечер, 2 ночь) | — |
| `temperature` | Датчик температуры | ветеринары | `temp`, `mode` | `cool`, `heat`, `off` |
| `turbidity` | Датчик загрязнённости воды | ветеринары | `turbidity`, NTU | — |
| `ph` | Датчик кислотности воды | ветеринары | `ph` | — |
| `filter` | Фильтр | ветеринары | `mode` (0 умеренная, 1 усиленная) | `boost`, `normal` |

Окно задаётся полем `section` устройства: `service` или `vet`. Уведомления адресуются так же (`to`).
`clock` — служебное устройство для сценариев по времени суток, переключается через `simulate`.

## Запуск

Бэкенд:

```bash
cd backend
python -m venv .venv
.venv/Scripts/pip install -r requirements.txt
.venv/Scripts/python -m uvicorn app.main:app --reload --port 8000
```

Фронт (Vue + Vite), в разработке — http://localhost:5173, запросы `/api` проксируются на бэкенд:

```bash
cd frontend
npm install
npm run dev
```

Сборка: `npm run build` в `frontend`. Если есть `frontend/dist`, бэкенд сам отдаёт фронт на http://localhost:8000.

Страницы: служебное, ветеринары, эмуляторы (задать показания датчиков), устройства (конструктор), сценарии, журнал.
Документация API: http://localhost:8000/docs.

## Файлы

- `devices.json` — устройства. Новое устройство — новая запись здесь, код писать не нужно.
- `scenarios.json` — стартовые сценарии.
- `data.json` — текущее состояние, создаётся само. Удалить файл или `POST /api/reset` — вернуться к стартовым данным.
- `app/models.py` — формат устройства и сценария.
- `app/engine.py` — изменение сигналов, события, запуск сценариев.
- `app/main.py` — ручки.
- `app/ujin.py` — отправка сигналов на стенд, включается `UJIN_LIVE=1` в `.env`.
- `ujin_check.py` — проверка подключения к стенду.

## Подключение к Ujin

Устройства привязаны к слотам стенда полем `ujin_ext`:

| Слот на стенде | Наши сигналы |
|---|---|
| `ry_leak_01` | протечка: `leak`, `water` |
| `ry_light_01` | свет: `level` |
| `ry_thermostat_01` | температура: `temp`, `mode` |
| `ry_counter_01` | вода: `turbidity`, `ph` |
| `ry_barrier_01` | вентиляция и фильтр: `humidity`, `fan`, `mode` |

Настройка в `.env` (образец — `.env.example`): `UJIN_UST` — токен резидента, `UJIN_LIVE=1` — отправлять сигналы.

- `python ujin_check.py` — показать настройки и что будет отправлено.
- `python ujin_check.py --send` — отправить текущие значения на стенд.

При `UJIN_LIVE=1` каждое изменение сигнала уходит на стенд, в журнале появляется строка «Ujin: отправлено …».
Тело запроса — JSON, `c` — класс модели `integrations_devices`, 0 отправляется как 0.001
(платформа не сохраняет 0), новый сигнал сначала создаётся коротким именем.

## Устройство

```json
{
  "id": "leak",
  "title": "Датчик протечки",
  "room": "Технический зал",
  "signals":  [{"name": "leak", "title": "Протечка", "values": {"0": "нет", "1": "есть"}},
               {"name": "water", "title": "Подача воды", "values": {"0": "перекрыта", "1": "открыта"}}],
  "events":   [{"name": "leak_detected", "title": "Обнаружена протечка", "when": {"leak": 1}}],
  "commands": [{"name": "water_off", "title": "Отключить воду", "set": {"water": 0}}],
  "settings": [],
  "online": true,
  "state": {"leak": 0, "water": 1},
  "updated": "14:35:02"
}
```

- `signals` — что устройство показывает. `values` — подписи для значений-списков, `unit` — единицы.
- `events` — событие наступает, когда сигналы стали равны `when`.
- `commands` — чем управляет: команда записывает в сигналы `set`, `"$value"` подставляется из запроса.
- `state` — текущие значения сигналов.

## Сценарий

```json
{
  "id": "leak",
  "title": "Протечка",
  "enabled": true,
  "when": {"type": "event", "device": "leak", "event": "leak_detected"},
  "if":   [],
  "then": [{"type": "command", "device": "leak", "command": "water_off"},
           {"type": "notify", "text": "Протечка в техническом зале, вода отключена"},
           {"type": "command", "device": "ventilation", "command": "fan_on"}],
  "last_run": "14:35:02",
  "last_result": "ok"
}
```

- `when.type`: `event` — событие устройства; `signal` — сигнал стал удовлетворять `op`/`value`
  (например, `temp > 26`); `manual` — только кнопкой.
- `if` — все условия должны выполняться. `op`: `==`, `!=`, `>`, `<`, `>=`, `<=`.
- `then`: `command` (устройство, команда, `value` при необходимости) или `notify` (`text`, `to` — кому, `service` или `vet`, по умолчанию `service`).
- `last_result`: `ok`, `skipped` (условие не выполнено), `error` (устройство недоступно — служебное окно получает уведомление).

## Ручки

| Метод | Путь | Что делает |
|---|---|---|
| GET | `/api/devices` | список устройств: название, сигналы, события, команды |
| GET | `/api/devices/{id}` | одно устройство с текущим `state` — для периодического опроса |
| GET | `/api/devices/{id}/history?minutes=60` | история значений для графиков: `{"temp": [[1793439105.3, 24], ...]}` |
| POST | `/api/devices` | создать устройство (тело — устройство целиком) |
| PUT | `/api/devices/{id}` | изменить описание (текущие значения сохраняются) |
| DELETE | `/api/devices/{id}` | удалить; 409, если используется в сценарии |
| POST | `/api/devices/{id}/command` | команда: `{"command": "water_off"}` или `{"command": "set_level", "value": 75}` |
| POST | `/api/devices/{id}/simulate` | эмуляция показаний: `{"leak": 1}`, `{"temp": 28}`, `{"period": 1}` |
| POST | `/api/devices/{id}/online` | связь с устройством: `{"online": false}` |
| GET | `/api/scenarios` | список сценариев |
| GET | `/api/scenarios/{id}` | один сценарий |
| POST | `/api/scenarios` | создать (`id` можно не передавать) |
| PUT | `/api/scenarios/{id}` | изменить |
| DELETE | `/api/scenarios/{id}` | удалить |
| POST | `/api/scenarios/{id}/run` | запустить вручную |
| GET | `/api/notifications` | уведомления (`?to=service` — служебному окну, `?to=vet` — ветеринарам) |
| GET | `/api/log` | журнал: события, команды, запуски |
| POST | `/api/reset` | вернуть стартовые данные |

История — точки `[время в секундах Unix, значение]`, новая точка появляется при каждом изменении сигнала.
Хранится в памяти (до 1000 точек на сигнал) и после перезапуска начинается заново с текущих значений.

Ошибки приходят как `{"detail": "текст"}` или `{"detail": ["текст", ...]}` для проверки сценария.

## Пример: протечка

```bash
curl -X POST localhost:8000/api/devices/leak/simulate -H "Content-Type: application/json" -d '{"leak": 1}'
curl localhost:8000/api/devices/leak          # water: 0 — вода отключена
curl localhost:8000/api/devices/ventilation   # fan: 1 — вентиляция включена
curl localhost:8000/api/notifications
```
