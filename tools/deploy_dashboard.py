#!/usr/bin/env python3
"""Publish both dashboards to Home Assistant.
1. Liquid Glass (main): copies dashboard/index.html (+ animations/*.json) to /config/www/liquid-glass/ over SSH and points the
   "liquid-glass" Webpage dashboard at it (cache-busting ?v=). The page detects Home Assistant and goes live.
2. Home (fallback): ha/dashboards/home.yaml with built-in cards; tiles for missing entities become placeholders.
Usage: python3 tools/deploy_dashboard.py
"""
import json, subprocess, sys, time
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
def ws(msg):
    r = subprocess.run([sys.executable, str(ROOT / "tools/ha.py"), json.dumps(msg)], capture_output=True, text=True)
    if r.returncode: sys.exit(r.stdout + r.stderr)
    return json.loads(r.stdout) if r.stdout.strip() else None

live = {e["entity_id"] for e in ws({"type": "config/entity_registry/list"})}
live |= {s["entity_id"] for s in ws({"type": "get_states"})}  # helpers and groups exist only as states
missing = []

def fix(card):
    if not isinstance(card, dict): return card
    if card.get("type") == "tile" and card["entity"] not in live:
        missing.append(card["entity"])
        return {"type": "button", "name": (card.get("name") or card["entity"].split(".", 1)[1].replace("_", " ").title()) + " · not paired yet",
                "icon": "mdi:link-variant-off", "tap_action": {"action": "none"}, "show_state": False}
    return card

cfg = yaml.safe_load((ROOT / "ha/dashboards/home.yaml").read_text())
for v in cfg["views"]:
    for s in v.get("sections", []):
        s["cards"] = [fix(c) for c in s["cards"]]

url = "dashboard-home"
if url not in {d["url_path"] for d in ws({"type": "lovelace/dashboards/list"})}:
    ws({"type": "lovelace/dashboards/create", "url_path": url, "title": "Home", "icon": "mdi:home", "show_in_sidebar": True, "require_admin": False})
ws({"type": "lovelace/config/save", "url_path": url, "config": cfg})
print("saved; placeholders for", len(missing), "missing entities:", sorted(set(missing)))

ssh = ["-i", str(Path("~/.ssh/ha_green").expanduser())]
subprocess.run(["ssh", *ssh, "root@192.168.178.57", "mkdir -p /config/www/liquid-glass/animations"], check=True)
subprocess.run(["scp", "-q", *ssh, str(ROOT / "dashboard/index.html"), "root@192.168.178.57:/config/www/liquid-glass/index.html"], check=True)
subprocess.run(["scp", "-q", *ssh, *map(str, sorted((ROOT / "dashboard/animations").glob("*.json"))), "root@192.168.178.57:/config/www/liquid-glass/animations/"], check=True)  # lottie files, loaded by relative path
if "liquid-glass" not in {d["url_path"] for d in ws({"type": "lovelace/dashboards/list"})}:
    ws({"type": "lovelace/dashboards/create", "url_path": "liquid-glass", "title": "Liquid Glass", "icon": "mdi:home-variant", "show_in_sidebar": True, "require_admin": False})
ws({"type": "lovelace/config/save", "url_path": "liquid-glass", "config": {"strategy": {"type": "iframe", "url": f"/local/liquid-glass/index.html?v={int(time.time())}"}}})
print("Liquid Glass page published")
