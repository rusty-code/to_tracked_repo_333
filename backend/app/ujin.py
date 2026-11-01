import os
import sys
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env")

CLS = os.getenv("UJIN_CLASS", "integrations_devices")
LIVE = os.getenv("UJIN_LIVE") == "1"
client = None
known = set()

if LIVE:
    # ujin_client.py лежит в emulators/ рядом с проектом или в корне репозитория
    for path in [os.getenv("EMULATORS_DIR", ""), ROOT / "emulators", ROOT.parent / "emulators"]:
        if path and (Path(path) / "ujin_client.py").exists():
            sys.path.insert(0, str(path))
            break
    from ujin_client import UjinClient

    if not os.getenv("UJIN_UST"):
        print("Ujin: UJIN_LIVE=1, но UJIN_UST пустой — заполните .env")
    client = UjinClient(os.getenv("UJIN_BASE_URL", "https://api-uae-test.ujin.tech"), dry_run=False,
                        cls=CLS, signal_prefix=CLS + "_", ust=os.getenv("UJIN_UST", ""),
                        apartment_id=os.getenv("UJIN_APARTMENT_ID", "2849"), logger=lambda *_: None)


def publish(d, values):
    """Отправить изменившиеся сигналы на стенд. Возвращает строку для журнала или None."""
    if not client or not d.ujin_ext:
        return None
    nums = {k: v for k, v in values.items() if isinstance(v, (int, float))}
    if not nums:
        return None
    # 0 платформа не сохраняет; новый сигнал сначала создаётся коротким именем
    rows = [{"sn": d.ujin_ext, "s": f"{CLS}_{k}", "v": v or 0.001, "c": CLS} for k, v in nums.items()]
    new = [{"sn": d.ujin_ext, "s": k, "v": 0.001, "c": CLS} for k in nums if (d.ujin_ext, k) not in known]
    short = ", ".join(f"{k}={v}" for k, v in nums.items())
    try:
        resp = client.publish_group(rows, new)
    except Exception as e:
        print("Ujin:", e)
        return f"Ujin: ошибка отправки {d.title} ({short}): {e}"
    if isinstance(resp, dict) and str(resp.get("error")) == "0":
        known.update((d.ujin_ext, k) for k in nums)
        return f"Ujin: отправлено {d.title} ({short})"
    print("Ujin:", resp)
    return f"Ujin: стенд не принял {d.title} ({short}): {resp}"
