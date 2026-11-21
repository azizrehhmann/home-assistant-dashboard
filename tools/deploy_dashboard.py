#!/usr/bin/env python3
"""Push ha/dashboards/home.yaml to Home Assistant. Tiles whose entity doesn't exist yet become a
'not paired yet' placeholder, so rerunning this after pairing more devices fills them in.
Usage: python3 tools/deploy_dashboard.py
"""
import json, subprocess, sys
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
