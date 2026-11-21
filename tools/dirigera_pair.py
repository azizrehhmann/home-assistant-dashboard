#!/usr/bin/env python3
"""Pair this Mac with the IKEA DIRIGERA local API (run, then press the hub's action button).

Saves the token to ~/.config/dirigera-token (0600). Never prints it.
Usage: python3 tools/dirigera_pair.py [hub-ip]
"""
import base64, hashlib, json, os, secrets, ssl, string, sys, time, urllib.parse, urllib.request
from pathlib import Path

IP = sys.argv[1] if len(sys.argv) > 1 else "192.168.178.39"
BASE = f"https://{IP}:8443/v1"
# shortcut: the hub uses a self-signed certificate, so verification is off; fine on the LAN, pin it if this goes beyond that.
CTX = ssl._create_unverified_context()

alphabet = string.ascii_letters + string.digits + "_-~."
verifier = "".join(secrets.choice(alphabet) for _ in range(128))
challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()

q = urllib.parse.urlencode({"audience": "homesmart.local", "response_type": "code",
                            "code_challenge": challenge, "code_challenge_method": "S256"})
code = json.load(urllib.request.urlopen(f"{BASE}/oauth/authorize?{q}", context=CTX, timeout=10))["code"]
print("PRESS THE ACTION BUTTON ON THE HUB NOW (60 s)", flush=True)

body = urllib.parse.urlencode({"code": code, "name": "claude-ha-deploy", "grant_type": "authorization_code",
                               "code_verifier": verifier}).encode()
for _ in range(32):
    time.sleep(2)
    try:
        req = urllib.request.Request(f"{BASE}/oauth/token", data=body,
                                     headers={"Content-Type": "application/x-www-form-urlencoded"})
        tok = json.load(urllib.request.urlopen(req, context=CTX, timeout=10))["access_token"]
    except Exception:
        continue
    path = Path("~/.config/dirigera-token").expanduser()
    path.parent.mkdir(exist_ok=True)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    os.write(fd, tok.encode()); os.close(fd)
    print("token saved")
    sys.exit(0)
sys.exit("timed out: button not pressed in time")
