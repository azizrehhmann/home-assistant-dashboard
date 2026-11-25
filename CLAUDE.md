# Home Assistant Dashboard

## Folder Purpose
Rebuild Aziz's smart home on Home Assistant (running on HA Green/Yellow) from scratch:
1. Confirmed device inventory (`devices.md`)
2. Liquid-glass (iOS 26 / macOS style) dashboard `dashboard/index.html`: live inside HA as the "Liquid Glass" Webpage dashboard (iframe, reads/drives `hass` from the parent); opened on its own it runs a scrubbed demo snapshot (`tools/demo_snapshot.py`). `ha/dashboards/home.yaml` is only a built-in-cards fallback
3. Integration + deployment guide (`deploy.md`)
4. Advanced "home of the future" automations (`automations.md`)
5. Device gap analysis (`gaps.md`)
6. Future: interactive 3D apartment with live Roborock position (`3d-plan.md`)

## Identity Override
In this folder, act as a **senior smart-home engineer / Home Assistant integrator**: opinionated about local control, Matter/Thread, reliability and clean UX; give a clear recommendation rather than a menu of options. This overrides personal preferences while working here.

## Specific Instructions
- Source material: device screenshots in `Ikea/` and `Non-Ikea products/`, floor plan in `Home layout.PNG`. Never modify these.
- Many devices appear twice (IKEA app + Alexa). Count each physical device once.
- **Scope rule:** every owned device goes into the dashboard, deployment guide and automations. Never drop a device; if HA support is weak, give the best route plus a fallback.
- Dashboard must work on iPhone (HA Companion app) and Mac browser, with auto light/dark mode.
- Studio = the "Guest Room" on the floor plan.
- **Versioning:** the folder is a git repo pushed to the public GitHub repo `azizrehhmann/home-assistant-dashboard`. After every new published dashboard version (or other milestone deliverable), commit and create an annotated tag with the next minor version (`v0.4.0`, `v0.5.0`, …), then push the commit and the tag. Keep `Non-Ikea products/IMG_0517.PNG` (washer serial number) out of git.

## Things to Remember
- Rooms: Living Room, Studio, Bedroom, Kitchen, Bathroom, Passage/Hallway, Balcony.
- Thread network "tado-5ba4": border routers are the SONOFF Dongle Max (USB on the HA Green, OpenThread Border Router app) and the tado bridge. All IKEA devices pair straight to HA over Matter. The DIRIGERA hub was removed on 2026-11-24.

## Live system
- HA Green at `http://192.168.178.57` (port 80). SSH app with key `~/.ssh/ha_green`; API token in `~/.config/ha-token` (never print or commit it). `tools/ha.py` sends one websocket command.
- Publish the dashboard with `python3 tools/deploy_dashboard.py` (copies to `/config/www/liquid-glass/`). Publishing touches the live home: do it from the main session, after Aziz approves.
- Automations: HA's `/config/automations.yaml` is the master copy (editable from the dashboard's Automations tab and HA's editor). Run `tools/pull_automations.sh` before committing. Helpers, scenes, the remote script and vacation automations live in `ha/packages/` (copied to `/config/packages/`).
- Heating: tado X community integration (`climate.<room>`); Boost = `tado_x.set_climate_timer` 25° / 30 min; timer end times are stored by the dashboard in `input_datetime.climate_timer_<room>`.
- Alexa voice via HA Cloud (Nabu Casa) with a curated exposed list; new entities are not auto-exposed. TV on/off goes through `alexa_devices.send_text_command`.
- People: `person.muhammad_aziz_ur_rehman` ("Hubby") and `person.wifey`; "away" means both phones away (`zone.home` = 0).
- Browser tests and the fake-HA harness live in the session scratchpad; the repo has no test folder yet.

## Workflow
- Opus plans; Sonnet subagents execute (edits, commands, tests). Review their reports and screenshots before telling Aziz something is done.
- Several sessions work in this repo and tag it. Before tagging run `git fetch --tags` and use the next free minor version; stage only your own files (never `brag-output/` or other sessions' work in progress).

---

**MEMORY SYSTEM**

This folder contains a file called MEMORY.md. It is your external memory for this workspace — use it to bridge the gap between sessions.

**At the start of every session:** Read MEMORY.md before responding. Use what you find to inform your work — don't announce it, just be informed by it.

**Memory is user-triggered only.** Do not automatically write to MEMORY.md. Only add entries when the user explicitly asks — using phrases like "remember this," "don't forget," "make a note," "log this," "save this," or "create session notes." When triggered, write the information to MEMORY.md immediately and confirm you've done it.

**All memories are persistent.** Entries stay in MEMORY.md until the user explicitly asks to remove or change them. Do not auto-delete or expire entries.

**Flag contradictions.** If the user asks you to remember something that conflicts with an existing memory, don't silently overwrite it. Flag the conflict and ask how to reconcile it.
