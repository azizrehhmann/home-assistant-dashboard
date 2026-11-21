# Home Assistant Dashboard

Rebuilding a flat's smart home on Home Assistant (HA Green) with a liquid-glass, iOS/macOS-style dashboard.

- `dashboard/index.html`: single-file interactive mock (mock data). Open it in a browser.
  It covers rooms, lights with warm/cool white and colour, tado heating, the Roborock with rooms, suction and passes, vacation mode, and a Three.js 3D floor plan.
- `devices.md`: confirmed device inventory and the HA integration for each.
- `Ikea/`, `Non-Ikea products/`, `Home layout.PNG`: source screenshots and the floor plan.

- `deploy.md`: step-by-step checklist to get every device into Home Assistant (HA Green, 2026.11+), with sources.
- `ha/themes/liquid_glass.yaml`: light/dark theme in the mock's colours (blur via card-mod).
- `ha/dashboards/home.yaml`: sections dashboard (built-in cards only) mirroring the mock.
- `ha/packages/`: helpers for vacation mode and Roborock room cleaning, scenes, plus ready-to-install automations (`automations.yaml`, `vacation_automations.yaml`).
- `automations.md`: catalogue of every automation (ready, next round, needs new devices) with test steps.

- `tools/`: `ha.py` (send one websocket command to HA), `deploy_dashboard.py` (publish the dashboard, with placeholders for unpaired devices), `dirigera_pair.py` (pair with the IKEA hub API).
- `gaps.md`: what the flat can't sense or control yet, ranked, with recommended devices and the automations they unlock.

Coming next: `3d-plan.md`.

## Versions
Each published dashboard version is tagged (`v0.3.0`, `v0.4.0`, …). See the GitHub releases/tags for the changelog.
