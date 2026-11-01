"""Проверка подключения к Ujin.

python ujin_check.py          — показать настройки и что будет отправлено (без сети)
python ujin_check.py --send   — отправить текущие значения всех устройств на стенд
"""
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")
for path in [os.getenv("EMULATORS_DIR", ""), ROOT / "emulators", ROOT.parent / "emulators"]:
    if path and (Path(path) / "ujin_client.py").exists():
        sys.path.insert(0, str(path))
        break
from ujin_client import UjinClient  # noqa: E402

CLS = os.getenv("UJIN_CLASS", "integrations_devices")
BASE = os.getenv("UJIN_BASE_URL", "https://api-uae-test.ujin.tech")
UST = os.getenv("UJIN_UST", "")
APT = os.getenv("UJIN_APARTMENT_ID", "2849")
send = "--send" in sys.argv

print(f"стенд:     {BASE}")
print(f"квартира:  {APT}")
print(f"класс:     {CLS}")
print(f"ust:       {'задан' if UST else 'ПУСТО — впишите UJIN_UST в .env'}")
print(f"UJIN_LIVE: {os.getenv('UJIN_LIVE', '0')} (1 — сервер публикует сигналы при каждом изменении)")
if send and not UST:
    sys.exit("Без UJIN_UST отправлять нельзя")

client = UjinClient(BASE, dry_run=not send, cls=CLS, signal_prefix=CLS + "_", ust=UST, apartment_id=APT,
                    logger=lambda *_: None)

devices = json.loads((ROOT / "backend" / "devices.json").read_text("utf-8"))
slots = {}
for d in devices:
    if d.get("ujin_ext"):
        slots.setdefault(d["ujin_ext"], {}).update(
            {k: v for k, v in d["state"].items() if isinstance(v, (int, float))})

ok = True
for ext, values in slots.items():
    new = [{"sn": ext, "s": k, "v": 0.001, "c": CLS} for k in values]
    rows = [{"sn": ext, "s": f"{CLS}_{k}", "v": v or 0.001, "c": CLS} for k, v in values.items()]
    resp = client.publish_group(rows, new)
    good = str(resp.get("error")) == "0" if isinstance(resp, dict) else False
    ok = ok and good
    print(f"{'OK ' if good else 'ERR'} {ext}: {', '.join(f'{k}={v}' for k, v in values.items())}"
          + ("" if good else f"  ответ: {resp}"))

if not send:
    print("\nЭто dry-run. Для отправки: python ujin_check.py --send")
elif ok:
    print("\nСтенд принял все сигналы. Проверьте значения в кабинете резидента квартиры", APT)
