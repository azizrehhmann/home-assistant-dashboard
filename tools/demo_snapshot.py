#!/usr/bin/env python3
"""Embed a scrubbed snapshot of the real home into dashboard/index.html (demo mode).

Usage:  python3 tools/demo_snapshot.py          (run from anywhere; token read from ~/.config/ha-token, never printed)
The repo is public: everything not on an allowlist is dropped, and the output is self-checked before it is written.
"""
import datetime, json, os, re, sys, urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
PAGE, AUTOS = ROOT / "dashboard" / "index.html", ROOT / "ha" / "automations.yaml"
URL = os.environ.get("HA_HTTP", "http://192.168.178.57")
MAX_BYTES = 150_000

DOMAINS = {"light", "switch", "climate", "sensor", "binary_sensor", "media_player", "vacuum", "person", "zone", "scene",
           "script", "automation", "update", "event", "weather", "select", "button", "sun", "input_boolean",
           "input_datetime", "input_number", "input_select", "input_text", "input_button", "fan"}
ATTRS = {"friendly_name", "device_class", "unit_of_measurement", "supported_color_modes", "color_mode", "brightness",
         "color_temp_kelvin", "hs_color", "rgb_color", "xy_color", "temperature", "current_temperature", "hvac_action",
         "manual_control_active", "current_humidity", "volume_level", "is_volume_muted", "media_title", "media_artist",
         "fan_speed", "id", "last_triggered", "entity_id", "options", "min", "max", "step", "has_date", "has_time",
         "icon", "installed_version", "latest_version", "title", "hvac_modes", "min_temp", "max_temp", "battery_level",
         "min_color_temp_kelvin", "max_color_temp_kelvin", "preset_mode", "preset_modes", "oscillating", "percentage"}
BAD_ID = re.compile(r"\d{10,}|fritz|gmail|@|iphone|phone|(^|[._])(ip|mac|ssid|bssid|wifi|gps)([._]|$)|device_tracker|bridge_x_\d")  # bridge_x_<serial> is a device serial
AUTO_KEYS = ("id", "alias", "description", "mode", "triggers", "conditions", "actions")
EMAIL = r"[\w.+-]+@[\w-]+\.[\w.-]+"
IPV4 = r"\b(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)\b"
FORBIDDEN = [r"[a-z_]+\.[a-z0-9_]*\d{10,}", r'"(latitude|longitude|gps|gps_accuracy|entity_picture|user_id)"', EMAIL, IPV4,
             r"[A-Za-z0-9+/=]{32,}", r"eyJ[A-Za-z0-9_-]{10,}"]


def scrub_states(raw):
    out = []
    for s in raw:
        eid = s["entity_id"]
        if eid.split(".")[0] not in DOMAINS or BAD_ID.search(eid.lower()):
            continue
        if "_segment_" in eid or re.search(r"(tv_lights|thermometer|govee).*_(connection_mode|connectivity|last_changed|snapshot|music_mode|music_sensitivity)|rate_limit", eid):  # Govee strip segments + diagnostics: never shown, only size
            continue
        if eid.startswith("button.") and "washing" not in eid:  # only the washer buttons are used; the rest is size
            continue
        a = {k: v for k, v in s["attributes"].items() if k in ATTRS}
        if eid.startswith("person."):
            a = {"friendly_name": a.get("friendly_name")}
        out.append({"entity_id": eid, "state": s["state"], "attributes": a,
                    "last_changed": s["last_changed"], "last_updated": s["last_updated"]})
    return out


def mask(v):
    """Autos are the user's own YAML: mask anything that looks like an email or IP instead of publishing it."""
    if isinstance(v, str):
        return re.sub(IPV4, "0.0.0.0", re.sub(EMAIL, "user@example.com", v))
    if isinstance(v, list):
        return [mask(x) for x in v]
    if isinstance(v, dict):
        return {k: mask(x) for k, x in v.items()}
    return v


def autos():
    return {c["id"]: mask({k: c[k] for k in AUTO_KEYS if k in c}) for c in yaml.safe_load(AUTOS.read_text())}


def check(blob):
    for pat in FORBIDDEN:
        m = re.search(pat, blob)
        if m:
            sys.exit(f"self-check failed ({pat[:30]}...): ...{blob[max(0, m.start() - 30):m.end() + 10]}...")
    if len(blob.encode()) > MAX_BYTES:
        sys.exit(f"too big: {len(blob.encode())} bytes > {MAX_BYTES}")


def embed(page, blob):
    blob = blob.replace("</", "<\\/")  # a literal </script> in data must not close the tag
    pat = re.compile(r"/\*DEMO-START\*/.*?/\*DEMO-END\*/", re.S)
    new = f"/*DEMO-START*/{blob}/*DEMO-END*/"
    if pat.search(page):
        return pat.sub(lambda _: new, page)
    # first run: add the data block just before the main script
    return page.replace('<script>\n', f'<script id="demo-data" type="application/json">{new}</script>\n<script>\n', 1) \
        if '<script>\n' in page else sys.exit("no <script> found")


def main():
    token = (Path.home() / ".config" / "ha-token").read_text().strip()
    req = urllib.request.Request(URL + "/api/states", headers={"Authorization": "Bearer " + token})
    raw = json.load(urllib.request.urlopen(req, timeout=20))
    data = {"date": datetime.date.today().isoformat(), "states": scrub_states(raw), "automations": autos()}
    blob = json.dumps(data, separators=(",", ":"), ensure_ascii=False)
    check(blob)
    page = PAGE.read_text()
    PAGE.write_text(embed(page, blob))
    print(f"demo snapshot {data['date']}: {len(data['states'])} entities, {len(data['automations'])} automations, {len(blob.encode())} bytes")


if __name__ == "__main__":
    main()
