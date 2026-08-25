import json
import os

import sounddevice as sd

CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")
SKIP_NAME = ("mapeador", "mapper", "primary", "primário", "mixagem", "stereo mix")


def load_config():
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_config(data):
    current = load_config()
    current.update(data)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(current, f, ensure_ascii=False, indent=2)


def list_input_devices():
    devices = []
    hostapis = sd.query_hostapis()
    for index, info in enumerate(sd.query_devices()):
        if info["max_input_channels"] < 1:
            continue
        name = (info["name"] or "").strip()
        if not name:
            continue
        lowered = name.lower()
        if any(skip in lowered for skip in SKIP_NAME):
            continue
        host = hostapis[info["hostapi"]]["name"]
        if host not in ("MME", "Windows WASAPI", "Windows DirectSound"):
            if "headset" not in lowered and "hands-free" not in lowered and "edifier" not in lowered:
                continue
        label = f"{name} ({host})"
        devices.append({"index": index, "name": name, "host": host, "label": label})
    return devices


def get_input_device_index():
    cfg = load_config()
    saved = cfg.get("input_device")
    devices = list_input_devices()
    if saved is not None:
        for dev in devices:
            if dev["index"] == saved:
                return saved
    default = sd.default.device[0]
    for dev in devices:
        if dev["index"] == default:
            return default
    return default


def set_input_device_index(index):
    save_config({"input_device": int(index)})
