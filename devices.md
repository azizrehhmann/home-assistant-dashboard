# Device Inventory

Confirmed with Aziz on 2026-11-21. Each physical device listed once (many also appear in Alexa via the IKEA skill).

**Platform:** Home Assistant on HA Green/Yellow · **Hub:** IKEA DIRIGERA (Hallway) — Matter bridge + Thread border router

| Room | Device | Ecosystem → HA integration |
|---|---|---|
| Bedroom | Bedroom light (ceiling) | IKEA → Matter |
| Bedroom | Bedside Lamp, Bedside Lamp 2 | IKEA → Matter |
| Bedroom | BILRESA dual button, BILRESA scroll wheel | IKEA → Matter (event entities) |
| Living | Living room light 1 + 2 (Alexa group "Living Room Ceiling") | IKEA → Matter |
| Living | BILRESA scroll wheel | IKEA → Matter |
| Living | Balcony door sensor (Alexa: "Living room door sensor") | IKEA → Matter |
| Living | Air Quality Monitor — **offline, re-pair first** | IKEA → Matter |
| Living | Living room lamp | Wi-Fi (Tuya or Tapo) |
| Living | TV lights — Govee LED strip behind TV | Govee lights local (LAN) / Govee cloud fallback |
| Living | Hisense TV (VIDAA OS) | Controlled via Alexa (`alexa_devices.send_text_command` on the living-room Echo): off/volume work; power-**on** needs the TV's Quick Start / network-standby setting, else an IR blaster. VIDAA integration needs Hisense's client cert (TV rejects any other), so not pursued. |
| Living | Philips soundbar HTL3320/10 ("Living Room Play-Fi") | TBC: Play-Fi / DLNA / Alexa; Bluetooth fallback |
| Living | Echo Dot | Alexa Devices |
| Kitchen | Kitchen ceiling light | IKEA → Matter |
| Kitchen | MYGGSPRAY motion sensor | IKEA → Matter |
| Kitchen | Rice cooker plug | Wi-Fi (Tuya or Tapo) |
| Kitchen | Siemens washing machine WG44B2040 | Home Connect (remote power-on works; starting needs Remote Start pressed on the machine) |
| Kitchen | Echo Dot | Alexa Devices |
| Hallway | Hallway light | IKEA → Matter (`light.hallway_light`, motion-controlled) |
| Hallway | Hallway motion sensor | IKEA → Matter |
| Hallway | Main Door Sensor | IKEA → Matter |
| Hallway | IKEA DIRIGERA hub | Matter bridge |
| Studio | Studio Lamp — one lamp, 3 IKEA bulbs (Alexa "Studio Lamp 1–3") | IKEA → Matter (HA light group) |
| Studio | Studio Light (ceiling) | IKEA → Matter |
| Studio | BILRESA scroll wheel | IKEA → Matter |
| Studio | Meross presence sensor, Matter-over-Thread, 3 zones | Matter (via DIRIGERA Thread) |
| Studio | Roborock Q5 Pro (dock) | Roborock |
| Studio | Echo Dot | Alexa Devices |
| Balcony | Balcony lights (LEDVANCE SMART+ Wi-Fi plug, Tuya-based) | Tuya, after moving the plug to the Smart Life app (local key is cloud-only) |
| Living, Studio, Bedroom, Bathroom | tado° X radiator thermostats (temp + humidity) | tado X (community) + Matter |

## Open items
- Living room lamp and rice cooker plug: TP-Link Kasa (local). Balcony lights: LEDVANCE (Tuya).
- Govee strip model (decides LAN vs cloud).
