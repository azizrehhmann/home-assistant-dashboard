# Home Assistant Dashboard

Rebuilding a flat's smart home on Home Assistant (HA Green) with a liquid-glass, iOS/macOS-style dashboard.

- `dashboard/index.html`: single-file interactive mock (mock data). Open it in a browser.
  It covers rooms, lights with warm/cool white and colour, tado heating, the Roborock with rooms, suction and passes, vacation mode, and a Three.js 3D floor plan.
- `devices.md`: confirmed device inventory and the HA integration for each.
- `Ikea/`, `Non-Ikea products/`, `Home layout.PNG`: source screenshots and the floor plan.

- `deploy.md`: step-by-step checklist to get every device into Home Assistant (HA Green, 2026.11+), with sources.
- `ha/themes/liquid_glass.yaml`: light/dark theme in the mock's colours (blur via card-mod).
- **Live dashboard:** `dashboard/index.html` doubles as the real dashboard. Inside Home Assistant (the "Liquid Glass" Webpage dashboard) it reads and controls real entities; opened on its own it runs **demo mode**: a scrubbed snapshot of the real home (no locations, emails, IPs or tokens) embedded in the page, fully interactive but nothing is sent anywhere. Refresh the snapshot with `python3 tools/demo_snapshot.py`. Publish with `python3 tools/deploy_dashboard.py`.
- **Appliance animations:** `dashboard/animations/` holds Lottie loops for the washer (idle, washing, rinsing, spinning, done) and the Roborock (docked, vacuuming, mopping, returning, charging), chosen from live state. lottie-web loads from cdnjs; without it the static icon shows. The deploy script copies them to `/config/www/liquid-glass/animations/`.
  - Home "Right now" activity strip (live only): animated cards for washer, robot, who is home, heating and music, shown only while true.
  - Home "Nerd stats" (live only, collapsible): entity counts, Thread, robot lifetime and consumables, batteries, internet, grid, 24 h sparklines.
  - Appliances Echo card: volume slider and mute per Echo Dot.
  - Climate: Boost/Timer countdown ("until 14:32 · 18 min left") stored in `input_datetime.climate_timer_<room>` (`ha/packages/climate_timers.yaml`), plus an "All thermometers" card.
- `ha/dashboards/home.yaml`: fallback dashboard with built-in cards only.
- `ha/automations.yaml`: snapshot of the live automations. Home Assistant is the master copy (edit them in the dashboard's Automations tab or HA's editor); refresh with `tools/pull_automations.sh`.
- `ha/packages/`: `climate_timers.yaml` (Boost/Timer end times), helpers (vacation, wake-up light, Roborock rooms), scenes, the remote script, and `vacation_automations.yaml` (not installed yet).
- `automations.md`: catalogue of every automation (ready, next round, needs new devices) with test steps.

- `tools/`: `ha.py` (send one websocket command to HA), `deploy_dashboard.py` (publish the dashboard, with placeholders for unpaired devices), `pull_automations.sh` (pull `automations.yaml` from HA), `demo_snapshot.py` (scrub and embed the demo data), `dirigera_pair.py` (pair with the IKEA hub API).
- `gaps.md`: what the flat can't sense or control yet, ranked, with recommended devices and the automations they unlock.

Coming next: `3d-plan.md`.

## Versions
Each published dashboard version is tagged (`v0.3.0`, `v0.4.0`, …). See the GitHub releases/tags for the changelog.
