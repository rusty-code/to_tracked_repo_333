import json
import time
from datetime import datetime
from pathlib import Path

from . import ujin
from .models import Device, Scenario

BASE = Path(__file__).resolve().parents[1]
DATA = BASE / "data.json"


def now():
    return datetime.now().strftime("%H:%M:%S")


def compare(a, op, b):
    try:
        a, b = float(a), float(b)
    except (TypeError, ValueError):
        a, b = str(a), str(b)
    return {"==": a == b, "!=": a != b, ">": a > b, "<": a < b, ">=": a >= b, "<=": a <= b}[op]


def match(state, when):
    return all(k in state and compare(state[k], "==", v) for k, v in when.items())


class Engine:
    def __init__(self):
        self.devices: dict[str, Device] = {}
        self.scenarios: dict[str, Scenario] = {}
        self.notifications = []
        self.log = []
        self.load()

    def load(self):
        if DATA.exists():
            data = json.loads(DATA.read_text("utf-8"))
        else:
            data = {"devices": json.loads((BASE / "devices.json").read_text("utf-8")),
                    "scenarios": json.loads((BASE / "scenarios.json").read_text("utf-8"))}
        self.devices = {d["id"]: Device(**d) for d in data["devices"]}
        self.scenarios = {s["id"]: Scenario(**s) for s in data["scenarios"]}
        self.history = {}  # устройство → сигнал → [[время, значение]], только в памяти
        for d in self.devices.values():
            self.remember(d, d.state)

    def remember(self, d, values):
        t = round(time.time(), 1)
        for k, v in values.items():
            points = self.history.setdefault(d.id, {}).setdefault(k, [])
            points.append([t, v])
            del points[:-1000]

    def save(self):
        DATA.write_text(json.dumps({
            "devices": [d.model_dump() for d in self.devices.values()],
            "scenarios": [s.model_dump(by_alias=True) for s in self.scenarios.values()],
        }, ensure_ascii=False, indent=1), "utf-8")

    def reset(self):
        DATA.unlink(missing_ok=True)
        self.notifications.clear()
        self.log.clear()
        self.load()

    def add_log(self, text):
        self.log.insert(0, {"time": now(), "text": text})
        del self.log[200:]

    def notify(self, to, text, scenario=""):
        self.notifications.insert(0, {"time": now(), "to": to, "text": text, "scenario": scenario})
        del self.notifications[100:]
        self.add_log(f"Уведомление ({to}): {text}")

    def write(self, d: Device, values: dict, depth=0):
        before = dict(d.state)
        changed = {k: v for k, v in values.items() if before.get(k) != v}
        if not changed:
            return
        d.state.update(changed)
        d.updated = now()
        self.remember(d, changed)
        self.save()
        if not d.online:
            return
        sent = ujin.publish(d, changed)
        if sent:
            self.add_log(sent)

        for ev in d.events:
            if ev.when and match(d.state, ev.when) and not match(before, ev.when):
                self.add_log(f"{d.title}: {ev.title or ev.name}")
                for sc in list(self.scenarios.values()):
                    w = sc.when
                    if sc.enabled and w.type == "event" and w.device == d.id and w.event == ev.name:
                        self.run(sc, depth)

        for sc in list(self.scenarios.values()):
            w = sc.when
            if not (sc.enabled and w.type == "signal" and w.device == d.id and w.signal in changed):
                continue
            was = w.signal in before and compare(before[w.signal], w.op, w.value)
            if compare(d.state[w.signal], w.op, w.value) and not was:
                self.run(sc, depth)

    def command(self, d: Device, name, value=None, depth=0):
        cmd = next((c for c in d.commands if c.name == name), None)
        if not cmd:
            raise ValueError(f"У «{d.title}» нет команды {name}")
        if not d.online:
            raise ValueError(f"«{d.title}» не в сети")
        self.add_log(f"{d.title} ← {cmd.title or name}" + (f" = {value}" if value is not None else ""))
        self.write(d, {k: value if v == "$value" else v for k, v in cmd.set.items()}, depth)

    def set_online(self, d: Device, online):
        d.online = online
        self.add_log(f"{d.title}: {'снова в сети' if online else 'нет связи'}")
        if not online:
            self.notify("service", f"Нет связи с устройством «{d.title}» ({d.room})")
        self.save()

    def check(self, c):
        d = self.devices.get(c.device)
        return d is not None and c.signal in d.state and compare(d.state[c.signal], c.op, c.value)

    def run(self, sc: Scenario, depth=0):
        if depth > 5:  # сценарии запускают друг друга по кругу
            self.add_log(f"«{sc.title}»: слишком длинная цепочка, остановлено")
            return
        sc.last_run = now()
        failed = next((c for c in sc.if_ if not self.check(c)), None)
        if failed:
            sc.last_result = "skipped"
            self.add_log(f"«{sc.title}» пропущен: не выполнено условие {failed.device}.{failed.signal}")
            return
        self.add_log(f"Запуск «{sc.title}»")
        sc.last_result = "ok"
        for a in sc.then:
            if a.type == "notify":
                self.notify(a.to, a.text, sc.title)
                continue
            try:
                d = self.devices.get(a.device)
                if not d:
                    raise ValueError(f"нет устройства {a.device}")
                self.command(d, a.command, a.value, depth + 1)
            except ValueError as e:
                sc.last_result = "error"
                self.notify("service", f"«{sc.title}» не выполнен до конца: {e}", sc.title)
        self.save()
