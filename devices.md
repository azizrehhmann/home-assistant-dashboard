# Device Inventory

Confirmed with Aziz on 2026-11-21. Each physical device listed once (many also appear in Alexa via the IKEA skill).

**Platform:** Home Assistant on HA Green/Yellow · **Thread:** network "tado-5ba4", border routers = SONOFF Dongle Max (USB on the HA Green, OpenThread Border Router app) + tado Internet Bridge X. All IKEA devices are paired straight to HA over Matter. DIRIGERA removed 2026-11-24 (failover tested with the Sonoff alone)

| Room | Device | Ecosystem → HA integration |
|---|---|---|
| Bedroom | Bedroom light (ceiling) | IKEA → Matter |
| Bedroom | Bedside Lamp, Bedside Lamp 2 | IKEA → Matter |
| Bedroom | BILRESA dual button, BILRESA scroll wheel | IKEA → Matter (event entities) |
| Living | Living room light 1 + 2 (Alexa group "Living Room Ceiling") | IKEA → Matter |
| Living | BILRESA scroll wheel | IKEA → Matter |
| Living | Balcony door sensor (Alexa: "Living room door sensor") | IKEA → Matter |
| Living | ALPSTUGA air quality monitor — online (Matter over Thread) | IKEA → Matter |
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
| Living room / Kitchen / Studio | Echo Dot ×3 + Alexa group "Everywhere" | Alexa Devices (now playing and controls); playback started via `send_text_command`; YouTube Music library (Music Assistant) played on Spotify |
| Hallway | Hallway light | IKEA → Matter (`light.hallway_light`, motion-controlled) |
| Hallway | Hallway motion sensor | IKEA → Matter |
| Hallway | Main Door Sensor | IKEA → Matter |
| Hallway | ~~IKEA DIRIGERA hub~~ | Removed 2026-11-24 (returned); replaced by the SONOFF Dongle Max as Thread border router |
| Studio | Studio Lamp — one lamp, 3 IKEA bulbs (Alexa "Studio Lamp 1–3") | IKEA → Matter (HA light group) |
| Studio | Studio Light (ceiling) | IKEA → Matter |
| Studio | BILRESA scroll wheel | IKEA → Matter |
| Studio | Meross presence sensor, Matter-over-Thread, 3 zones | Matter over Thread |
| Studio | Roborock Q5 Pro (dock) | Roborock |
| Studio | Echo Dot | Alexa Devices |
| Balcony | Balcony lights (LEDVANCE SMART+ Wi-Fi plug, Tuya-based) | Tuya, after moving the plug to the Smart Life app (local key is cloud-only) |
| Living, Studio, Bedroom, Bathroom | tado° X radiator thermostats (temp + humidity) | tado X (community) + Matter |

## Pairing status (2026-11-25)
**In Home Assistant:** all IKEA lights (including Living Room Light 2 and Studio Light), the remotes, door and motion sensors, the ALPSTUGA, the Meross presence sensor, tado X, the Roborock, the Siemens washer, the 3 Echo Dots, the Kasa lamp and the rice cooker plug.

**Still missing:** Govee TV lights, the LEDVANCE balcony plug, the Philips HTL3320 soundbar, and the Hisense TV as a media player (on/off already works through Alexa).

## Open items
- Pair the LEDVANCE balcony plug (Tuya, via Smart Life) and the Govee TV lights (decide LAN vs cloud from the strip model).
- Philips HTL3320 soundbar: no HA route chosen yet.
- Hisense TV as a real media player (today: on/off via Alexa only).
