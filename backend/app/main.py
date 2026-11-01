import time
import uuid
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

from .engine import Engine
from .models import Device, Scenario

app = FastAPI(title="Связка")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
engine = Engine()


class CommandIn(BaseModel):
    command: str
    value: Any = None


class OnlineIn(BaseModel):
    online: bool


def get_device(device_id):
    if device_id not in engine.devices:
        raise HTTPException(404, "Устройство не найдено")
    return engine.devices[device_id]


def get_scenario(scenario_id):
    if scenario_id not in engine.scenarios:
        raise HTTPException(404, "Сценарий не найден")
    return engine.scenarios[scenario_id]


def check(sc: Scenario):
    errors, devs = [], engine.devices
    w = sc.when
    if w.type != "manual":
        d = devs.get(w.device)
        if not d:
            errors.append(f"Когда: нет устройства {w.device}")
        elif w.type == "event" and w.event not in [e.name for e in d.events]:
            errors.append(f"Когда: у «{d.title}» нет события {w.event}")
        elif w.type == "signal" and w.signal not in [s.name for s in d.signals]:
            errors.append(f"Когда: у «{d.title}» нет сигнала {w.signal}")
    for c in sc.if_:
        d = devs.get(c.device)
        if not d or c.signal not in [s.name for s in d.signals]:
            errors.append(f"Если: нет сигнала {c.device}.{c.signal}")
    for a in sc.then:
        d = devs.get(a.device)
        if a.type == "command" and (not d or a.command not in [x.name for x in d.commands]):
            errors.append(f"То: нет команды {a.device}.{a.command}")
        if a.type == "notify" and not a.text:
            errors.append("То: пустой текст уведомления")
    if not sc.then:
        errors.append("То: нужно хотя бы одно действие")
    if errors:
        raise HTTPException(400, errors)


# устройства

@app.get("/api/devices", response_model=list[Device])
def list_devices():
    return list(engine.devices.values())


@app.get("/api/devices/{device_id}", response_model=Device)
def device(device_id: str):
    return get_device(device_id)


@app.get("/api/devices/{device_id}/history")
def device_history(device_id: str, minutes: int = 60):
    get_device(device_id)
    since = time.time() - minutes * 60
    return {k: [p for p in points if p[0] >= since]
            for k, points in engine.history.get(device_id, {}).items()}


@app.post("/api/devices", response_model=Device, status_code=201)
def create_device(d: Device):
    if d.id in engine.devices:
        raise HTTPException(409, "Устройство с таким id уже есть")
    engine.devices[d.id] = d
    engine.remember(d, d.state)
    engine.save()
    return d


@app.put("/api/devices/{device_id}", response_model=Device)
def update_device(device_id: str, d: Device):
    old = get_device(device_id)
    d.id, d.online, d.state = device_id, old.online, {**d.state, **old.state}
    engine.devices[device_id] = d
    engine.save()
    return d


@app.delete("/api/devices/{device_id}")
def delete_device(device_id: str):
    get_device(device_id)
    used = [s.title for s in engine.scenarios.values()
            if device_id in {s.when.device, *(c.device for c in s.if_), *(a.device for a in s.then)}]
    if used:
        raise HTTPException(409, "Устройство используется в сценариях: " + ", ".join(used))
    del engine.devices[device_id]
    engine.history.pop(device_id, None)
    engine.save()
    return {"ok": True}


@app.post("/api/devices/{device_id}/command", response_model=Device)
def command(device_id: str, body: CommandIn):
    d = get_device(device_id)
    try:
        engine.command(d, body.command, body.value)
    except ValueError as e:
        raise HTTPException(400, str(e))
    return d


@app.post("/api/devices/{device_id}/simulate", response_model=Device)
def simulate(device_id: str, values: dict[str, Any]):
    d = get_device(device_id)
    engine.write(d, values)
    return d


@app.post("/api/devices/{device_id}/online", response_model=Device)
def set_online(device_id: str, body: OnlineIn):
    d = get_device(device_id)
    engine.set_online(d, body.online)
    return d


# сценарии

@app.get("/api/scenarios", response_model=list[Scenario])
def list_scenarios():
    return list(engine.scenarios.values())


@app.get("/api/scenarios/{scenario_id}", response_model=Scenario)
def scenario(scenario_id: str):
    return get_scenario(scenario_id)


@app.post("/api/scenarios", response_model=Scenario, status_code=201)
def create_scenario(sc: Scenario):
    check(sc)
    sc.id = sc.id or uuid.uuid4().hex[:8]
    engine.scenarios[sc.id] = sc
    engine.save()
    return sc


@app.put("/api/scenarios/{scenario_id}", response_model=Scenario)
def update_scenario(scenario_id: str, sc: Scenario):
    old = get_scenario(scenario_id)
    check(sc)
    sc.id, sc.last_run, sc.last_result = scenario_id, old.last_run, old.last_result
    engine.scenarios[scenario_id] = sc
    engine.save()
    return sc


@app.delete("/api/scenarios/{scenario_id}")
def delete_scenario(scenario_id: str):
    get_scenario(scenario_id)
    del engine.scenarios[scenario_id]
    engine.save()
    return {"ok": True}


@app.post("/api/scenarios/{scenario_id}/run", response_model=Scenario)
def run_scenario(scenario_id: str):
    sc = get_scenario(scenario_id)
    engine.run(sc)
    return sc


# уведомления и журнал

@app.get("/api/notifications")
def notifications(to: str = ""):
    return [n for n in engine.notifications if not to or n["to"] == to]


@app.get("/api/log")
def log():
    return engine.log


@app.post("/api/reset")
def reset():
    engine.reset()
    return {"ok": True}


# собранный фронт (npm run build), если он есть
DIST = Path(__file__).resolve().parents[2] / "frontend" / "dist"
if DIST.exists():
    @app.get("/{path:path}", include_in_schema=False)
    def frontend(path: str):
        f = DIST / path
        return FileResponse(f if path and f.is_file() else DIST / "index.html")
