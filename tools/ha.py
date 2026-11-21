#!/usr/bin/env python3
"""Send one websocket command to Home Assistant and print the JSON result.

Usage:  python3 tools/ha.py '{"type": "config/area_registry/list"}'
        python3 tools/ha.py @payload.json
Token is read from ~/.config/ha-token (never printed). HA_URL overrides the host.
"""
import asyncio, json, os, sys
from pathlib import Path

import websockets

URL = os.environ.get("HA_URL", "ws://192.168.178.57/api/websocket")
TOKEN = Path("~/.config/ha-token").expanduser().read_text().strip()


async def call(msg: dict):
    async with websockets.connect(URL, max_size=None) as ws:
        assert json.loads(await ws.recv())["type"] == "auth_required"
        await ws.send(json.dumps({"type": "auth", "access_token": TOKEN}))
        auth = json.loads(await ws.recv())
        if auth["type"] != "auth_ok":
            sys.exit(f"auth failed: {auth.get('message')}")
        await ws.send(json.dumps({"id": 1, **msg}))
        while True:
            r = json.loads(await ws.recv())
            if r.get("id") == 1 and r["type"] == "result":
                return r


if __name__ == "__main__":
    arg = sys.argv[1]
    msg = json.loads(Path(arg[1:]).read_text() if arg.startswith("@") else arg)
    r = asyncio.run(call(msg))
    print(json.dumps(r.get("result") if r["success"] else r.get("error"), indent=1))
    sys.exit(0 if r["success"] else 1)
