# Deployment guide: every device into Home Assistant

> **Status as of 2026-11-25.** Done: HA Green running, IKEA devices paired straight over Matter (DIRIGERA removed), Thread via the SONOFF Dongle Max, tado X, Roborock, washer, Echo Dots, Kasa plugs, live "Liquid Glass" dashboard, automations. Left: Govee TV lights, LEDVANCE balcony plug, Philips HTL3320, Hisense TV as media player. The checklist below is the original plan, kept as history.


Target: **Home Assistant Green**, HA **2026.11 or newer**. Researched 2026-11-21; sources at the end.
Work through the phases in order and tick the boxes. Allow 3–4 hours in total; Phase B is the longest.

**Have ready before you start**
- [ ] iPhone with the **Home Assistant Companion app**, logged in to your HA. Matter pairing only works from the app, not from a browser.
- [ ] IKEA Home smart app, Meross app, Smart Life and/or Tapo app, Govee Home app, Roborock app, Home Connect app, Alexa app.
- [ ] Amazon account set to **authenticator-app 2-step verification** (SMS codes do not work with HA).
- [ ] A free **Home Connect developer account** (Phase C2 explains it).

---

## Phase 0: one purchase I recommend: Home Assistant Connect ZBT-2

IKEA's new Thread devices are the BILRESA buttons and wheels, the MYGGSPRAY motion sensors, the door sensors, and the Meross presence sensor. Shared from DIRIGERA into HA, they often **stop updating after a few minutes** ("subscription liveness timeout"). Restarting HA's Matter server only helps for a while, and IKEA firmware has not fixed it yet. People who give HA its own Thread radio report these devices as stable. The HA Green has no radio built in.

- **Plan:** do Phase B with DIRIGERA first. If any Thread device goes "unavailable" within a day, do **B7** (move the Thread devices onto a ZBT-2).
- Bonus: with a ZBT-2, HA can update IKEA Thread firmware itself.

---

## Phase A: preparation

1. [ ] **Update** HA: Settings → System → Updates. Install Core 2026.11+ and the OS update.
2. [ ] **Back up**: Settings → System → Backups → Backup now. Keep a copy off the Green.
3. [ ] **IPv6 on**: Settings → System → Network → IPv6 = *Automatic*. Matter and Thread need it.
4. [ ] **Router**:
   - Give fixed IP addresses (DHCP reservations) to the HA Green, DIRIGERA, Hisense TV, Govee strip and the Wi-Fi plug/lamps.
   - Turn **off** any "multicast optimisation", "IGMP snooping", "AP isolation" or "client isolation" on the Wi-Fi.
   - Keep everything on one network (no guest network, no separate VLAN).
5. [ ] **Areas** (Settings → Areas, labels & zones). Create them with exactly these IDs so the dashboard YAML matches:
   `living_room`, `studio`, `bedroom`, `kitchen`, `bathroom`, `hallway`, `balcony`.
6. [ ] **File access**: Settings → Apps (formerly Add-ons) → install **File editor** or **Studio Code Server**.
7. [ ] **Packages**: add this to `configuration.yaml`, then copy this repo's `ha/packages/` folder to `/config/packages/`:
   ```yaml
   homeassistant:
     packages: !include_dir_named packages
   ```
   Restart HA. This creates the helpers for vacation mode and robot room cleaning (Phase E).
8. [ ] **Marketplace** (HACS is built into HA since 2026.11): Settings → Marketplace. Catalog installs need no GitHub account. "Add from link" asks you to sign in to GitHub once.

---

## Phase B: IKEA (DIRIGERA) and Meross over Matter

> **Update 2026-11-24:** done differently. Every IKEA device is paired straight to HA (none via the DIRIGERA bridge). Thread border routers are now the **SONOFF Dongle Max** (OpenThread RCP firmware, USB on the HA Green, OpenThread Border Router app, 460800 baud, flow control off, joined to the existing tado-5ba4 network) and the tado bridge. The DIRIGERA was removed after a failover test with the Sonoff as the only border router. Firmware updates for IKEA devices come through HA's Matter update entities.

**How it works:**
- DIRIGERA acts as a **Matter bridge** for its **Zigbee** devices. They all arrive in HA together with one code.
- Native **Matter-over-Thread** devices are **not** part of the bridge. Each needs its **own sharing code** from the IKEA app.
- Which of your bulbs are Zigbee or Thread doesn't matter: anything missing after B3 gets shared individually in B4.

1. [ ] Settings → Apps → install **Matter Server**, then start it.
2. [ ] Settings → Devices & services → **Matter** should appear. Add it if it doesn't.
3. [ ] **Bridge**:
   - IKEA app → Settings → Integrations → **Matter bridge** → create a pairing code.
   - Companion app on the iPhone → Settings → Devices & services → Add integration → **Add Matter device** → *"It's already in use"* → enter the code.
   - Wait 1–2 minutes.
4. [ ] **Thread devices, one by one.** For each device below that did not appear with the bridge:
   - IKEA app → device → settings → *Share / pair with another platform* → copy its code.
   - Companion app → Add Matter device → *already in use* → enter the code.
   - Repeat for every device:
     - 4 BILRESA remotes: bedroom dual button, and the bedroom, living room and studio scroll wheels
     - MYGGSPRAY motion sensors (kitchen, hallway)
     - door sensors (main door, balcony door)
     - Air Quality Monitor, **after** fixing it in B6
     - any lights still missing
5. [ ] **Meross MS605 presence sensor**: share it the same way, from the app it currently lives in (IKEA or Meross).
   - Expect three occupancy entities (zones 1–3) and an illuminance entity.
   - In the Meross app, set the **light-level reporting interval to 2 minutes** and tune each zone's range and hold time. Only the Meross app can change these.
6. [ ] **Air Quality Monitor (offline)**: power-cycle it next to DIRIGERA. If it stays offline, remove it in the IKEA app and add it again. Then share it (B4).
   - VINDSTYRKA (Zigbee) arrives through the bridge. ALPSTUGA (Thread) needs its own code.
7. [ ] **Only if Thread devices drop out (ZBT-2 path)**:
   - Plug the ZBT-2 into the Green using its USB extension cable, away from the Green's metal and Wi-Fi.
   - HA offers it → **Use as Thread adapter**. This installs the OpenThread Border Router app.
   - Settings → Devices & services → **Thread** → make the HA network the **preferred** network.
   - Companion app → Settings → Companion app → Troubleshooting → **Sync Thread credentials**.
   - For each Thread device: remove it from HA and from the IKEA app, factory-reset it, then add it directly in HA (Companion app → Add Matter device → scan its QR code) **standing next to the Green**.
   - DIRIGERA then keeps only the Zigbee bridge.
8. [ ] **BILRESA buttons and wheels**:
   - Open each remote's device page → *Entities not shown* → **enable all event entities** (the wheel has about 9).
   - The built-in support only reports a turn after you stop turning, up to 8 steps. For live dimming, install **IKEA BILRESA** from Marketplace → *Add from link* → `https://github.com/Vituhlos/ha-ikea-bilresa`. It needs HA 2026.8+ and adds rotate_up/down plus press, double, triple and hold.
9. [ ] **Avoid duplicates**: don't share a device into HA a second way, such as through Alexa or Apple Home as well.
10. [ ] **Remove the Alexa duplicates later**: once HA works, Alexa can get everything from HA (or keep the IKEA skill). Remove the second copies in the Alexa app so voice commands don't double up.

---

## Phase C: the other integrations

### C1. tado° X heating (done 2026-11-22)
The flat has **tado X** (4 Smart Radiator Thermostats X + Bridge X). Two routes run side by side:
1. [x] **Matter (local):** each thermostat added to HA as a Matter device. Heat/off and target only. Entities are `climate.<room>_matter` (hidden); they keep working if tado's cloud is down.
2. [x] **tado X integration (cloud, community):** the official tado integration loops on "Device login flow status is PENDING" with tado X, so it was removed. Instead, [exabird/ha-tado-x](https://github.com/exabird/ha-tado-x) v1.8.11 lives in `/config/custom_components/tado_x` (Marketplace route: Add from link). Approve the tado login link once.
   - `climate.<room>`: modes `auto` (= tado schedule), `heat`, `off`. A target change is a 30-minute timer, as in the tado app.
   - Per-room boost: `tado_x.set_climate_timer` with 25 °C for 30 min.
   - Home-wide: `button.home_boost_all`, `button.home_turn_off_all`, `button.home_resume_schedules`.
   - Uses about 30 API calls per hour of the 20,000/day quota (`sensor.home_home_api_quota_remaining`).
3. [x] The official tado DHCP discovery is set to *ignored*, so it stops prompting.
- If one thermostat goes "unavailable" over HomeKit: delete `.storage/homekit_controller-entity-map` and pair again.

### C2. Siemens washing machine (Home Connect)
1. [ ] Sign up at **developer.home-connect.com**. Under *Default Home Connect User Account for Testing*, enter your Home Connect app e-mail in **lowercase**.
2. [ ] Register an application:
   - *Authorization Code Grant Flow*
   - Redirect URI `https://my.home-assistant.io/redirect/oauth`
   - Copy the Client ID and Secret, then **log out of the portal** (otherwise you get `unauthorized_client`).
3. [ ] Wait **15 minutes**. Then add the **Home Connect** integration and enter the ID and Secret when asked for application credentials.
4. [ ] You get:
   - operation state, door, finish time, program progress
   - an **"program finished" event**, which triggers the Echo announcement
   - selects for program, temperature and spin, plus pause/resume/stop buttons
   - There is no "remaining time" sensor; the dashboard works it out from the finish time.
- **Remote start**: power on, close the door and press *Remote Start* on the machine; this has to be re-armed after each door opening. Then start from HA.

### C3. Roborock Q5 Pro
1. [ ] Add **Roborock** → your app e-mail → enter the code Roborock e-mails you. Region: Auto.
2. [ ] **Room IDs**: Tools → Actions → `roborock.get_maps` with *return response* on. Note the segment ID of each room. Put them into `ha/packages/roborock.yaml` (the `segment_ids` block) and reload scripts.
3. [ ] Optional, for voice ("clean the kitchen"): vacuum entity → settings → **Map vacuum segments to areas**. This enables `vacuum.clean_area`, which doesn't do multiple passes; the dashboard uses the script, which does.
4. [ ] **Suction names**: Tools → States → the vacuum → `fan_speed_list`. Copy the exact strings into `input_select.robot_suction` in `roborock.yaml` if they differ from `quiet / balanced / turbo / max / max_plus`.
- You also get a **live map image**, area/time/error/consumable sensors, and buttons for your app routines.
- There is no fast live-position feed (updates come every 30 s through the cloud). That's the constraint for the 3D phase.

### C4. Wi-Fi devices: living room lamp, balcony lights, rice-cooker plug
Check which app controls each device: **Tapo** or **Smart Life**.
- [ ] **Tapo / Kasa**:
  - Tapo app → Me → *Tapo Lab* → turn on **Third-Party Compatibility**.
  - HA discovers the devices; enter your TP-Link e-mail (case-sensitive) and password. This is local control.
- [ ] **Smart Life (Tuya)**:
  - Smart Life → Me → ⚙ → Account and Security → copy the **User Code**.
  - HA → add **Tuya** → enter the code → scan the QR code from Smart Life (+ → Scan).
  - This is cloud-only; reload the integration after adding new devices in the app.

### C5. Govee TV lights
1. [ ] Govee Home → the strip → Settings → turn on **LAN Control**.
2. [ ] HA → add **Govee lights local**. It discovers the strip (UDP ports 4001/4003 and multicast must be allowed).
- If your model has no LAN Control toggle: Govee Home → Profile → ⚙ → About us → *Apply for API key*, then install **Govee** from Marketplace (`LaggAt/hacs-govee`).

### C6. Echo Dots (announcements)
1. [ ] Make sure Amazon 2-step verification uses an **authenticator app**.
2. [ ] HA → add **Alexa Devices** → e-mail, password, one-time code.
3. [ ] Each Echo gets *Speak* and *Announce* notify entities, a media player and a do-not-disturb switch.
   - Announce plays a chime first.
   - Actions include `alexa_devices.send_text_command`, which lets HA "say" anything to Alexa, such as "turn on the TV".
   - "Failed to refresh communications" warnings are Amazon rate limiting and are harmless.

### C7. Hisense VIDAA TV
1. [ ] Give the TV a fixed IP and set its clock/timezone to match HA.
2. [ ] Marketplace → *Add from link* → `https://github.com/warrenrees/ha_vidaatv` → install → restart → add **Vidaa TV** → TV IP → enter the **PIN shown on the TV**. On older firmware, choose *Static* at the certificate step.
3. [ ] If pairing fails because your firmware needs a client certificate, use the **fallback**: control the TV through Alexa with `alexa_devices.send_text_command` ("turn off the TV", "set TV volume to 20"). It already works in your Alexa app.
- Power **on** through the network (Wake-on-LAN) only works on some models and usually needs Ethernet. Alexa is the reliable way to turn it on.

### C8. Philips HTL3320/10 soundbar
According to Philips, this model has **no Wi-Fi or Play-Fi**: only Bluetooth, USB and **HDMI ARC**. HA can't talk to it directly.
- [ ] Connect it to the TV's HDMI ARC port and turn on CEC/ARC in the TV settings. TV volume and power then control the soundbar, so the TV integration (C7) covers it.
- [ ] Check the Alexa app → Devices → **"Living Room Play-Fi"**. Its device type tells us what it really is (probably a different device). If it's Play-Fi capable, this section changes.

---

## Phase D: rename entities to match the dashboard

The dashboard and packages use these IDs. For each one: Settings → Entities → the entity → ⚙ → *Entity ID*. Assign each device to its area as you go.

| Entity ID | Device |
|---|---|
| `light.bedroom_ceiling` | Bedroom light |
| `light.bedside_lamp`, `light.bedside_lamp_2` | Bedside lamps |
| `light.living_room_light_1`, `light.living_room_light_2` | Living room ceiling |
| `light.living_room_lamp` | Wi-Fi lamp |
| `light.tv_lights` | Govee strip |
| `light.kitchen_ceiling` | Kitchen ceiling light |
| `light.studio_lamp` | Studio lamp (3 bulbs; if they arrive separately, group them: Helpers → Group → Light group) |
| `light.studio_light` | Studio ceiling light |
| `light.balcony_lights` | Balcony lights |
| `switch.rice_cooker` | Rice-cooker plug |
| `binary_sensor.main_door`, `binary_sensor.balcony_door` | Door sensors |
| `binary_sensor.hallway_motion`, `binary_sensor.kitchen_motion` | MYGGSPRAY sensors |
| `binary_sensor.studio_presence_zone_1/2/3` | Meross zones |
| `sensor.studio_illuminance` | Meross light level |
| `sensor.air_quality_monitor_pm25` (+ humidity/temperature) | IKEA air quality monitor |
| `climate.living_room`, `climate.studio`, `climate.bedroom`, `climate.bathroom` | tado X integration (Matter twins: `…_matter`, hidden) |
| `sensor.washer_operation_state`, `sensor.washer_finish_time`, `sensor.washer_program_progress`, `event.washer_program_finished` | Home Connect |
| `vacuum.roborock_q5_pro`, `image.roborock_q5_pro_map` | Roborock |
| `media_player.living_room_tv` | Hisense TV |
| `notify.kitchen_echo_dot_announce`, `notify.living_room_echo_dot_announce`, `notify.studio_echo_dot_announce` | Echo Dots |
| `event.bedroom_dual_button`, `event.bedroom_scroll_wheel`, `event.living_room_scroll_wheel`, `event.studio_scroll_wheel` | BILRESA (pick the main event entity of each) |

---

## Phase E: helpers (created by the packages from Phase A7)

- `ha/packages/vacation.yaml`:
  - `input_boolean.vacation_mode`
  - start and return dates
  - open-ended switch
  - robot interval and time
  - one switch per exception: security alerts, pre-heat (with hours), presence simulation, humidity alerts
  - The vacation **automations** come in `automations.md`.
- `ha/packages/roborock.yaml`:
  - a switch per room
  - suction choice and passes (1–3)
  - `script.robot_clean_selected_rooms`, which sends `app_segment_clean` with the selected rooms and `repeat`
- `ha/packages/scenes.yaml`: the mock's scenes (Morning, Focus, Movie, Night) and `script.away`, which the dashboard's scene buttons call.
- `ha/packages/automations.yaml` and `vacation_automations.yaml`: the ready automations. Replace the placeholders listed at the top of `automations.md` first.
- Check: Settings → Devices & services → **Helpers** lists them all.
- The Vacation button on the Home view links to `/dashboard-home/security`. If your dashboard's URL isn't `dashboard-home`, change that one line.

---

## Phase F: theme and dashboard

1. [ ] **Theme**:
   - Copy `ha/themes/liquid_glass.yaml` to `/config/themes/`.
   - Add `frontend: themes: !include_dir_merge_named themes` to `configuration.yaml` and restart.
   - Profile → Theme → **Liquid Glass**. Mode *Auto* follows the phone/Mac; *Light* and *Dark* force one, like the mock's switch.
2. [ ] **Frosted blur**:
   - Plain HA themes can't blur cards. Install **card-mod** from Marketplace; the theme already contains the blur rule.
   - If the blur doesn't show on your HA version (card-mod's theme hook broke in some 2026 releases), install **Frosted Glass themes** (`wessamlauf/homeassistant-frosted-glass-themes`) with its recommended UIX setup instead, and keep our colours. Never run UIX and card-mod together.
3. [ ] **Dashboard**:
   - Settings → Dashboards → Add dashboard → *New dashboard from scratch* → name it "Home".
   - Open it → ⋮ → Edit → ⋮ → **Raw configuration editor** → paste `ha/dashboards/home.yaml` → Save.
   - It uses built-in cards only, so HA updates won't break it.
4. [ ] **Make it the default**: Settings → Dashboards → "Home" → *Set as default* (on each device: Profile → Dashboard).
5. [ ] On the iPhone: Companion app → open the dashboard → check light/dark mode and that nothing scrolls sideways.

---

## Phase F2: Alexa voice control (HA Cloud) (done 2026-11-22)
1. [x] HA Cloud subscription active; a core restart was needed so the cloud connection starts.
2. [x] Auto-expose of new entities is **off**. Exposed to Alexa (21): room light groups, Kitchen light, Studio lamp, Bedside lamps, Rice cooker, scenes Morning / Focus mode / Movie mode / Night mode, Away mode, Robot, the four "… heating" thermostats, Wake-up light. Names set in the entity registry so they're easy to say.
3. [ ] **Alexa app** → More → Skills & games → search **Home Assistant** → Enable → sign in with the HA Cloud account → **Discover devices**.
4. [ ] Delete old IKEA/DIRIGERA devices in the Alexa app that no longer work, so names don't clash.
- Try: "Alexa, turn on the studio lamp", "Alexa, turn on movie mode", "Alexa, set bedroom heating to 21 degrees", "Alexa, start Robot".
- To add something later: Settings → Voice assistants → Expose.

## Phase G: final check

- [x] Every row in the Phase D table exists and is in the right area (Settings → Areas). (verified 2026-11-28: all room devices assigned; whole-home items like the Everywhere speaker group and light mode left without a room)
- [ ] Toggle each light from the dashboard; change warmth on one IKEA bulb. (partial 2026-11-28: all 13 IKEA lights turned on at least 4 times in the last 72 h; warmth change not verified)
- [x] Open a door → its sensor flips within 2 s. Walk past each motion sensor and through each presence zone. (verified 2026-11-28: main_door, balcony_door, hallway/kitchen motion and studio presence zone 1 all changed state in the last 72 h; latency not measured; studio presence zones 2 and 3 never triggered)
- [x] Leave the Thread devices for 24 h → none shows "unavailable". If one does, do B7. (verified 2026-11-28: no unavailable transitions in the last 24 h; only the ALPSTUGA air quality monitor dropped, 4 times about 37 h ago)
- [ ] Run `script.robot_clean_selected_rooms` with one room and 1 pass. (2026-11-28: script exists, state off; not run)
- [ ] Send a test announcement: Tools → Actions → `notify.send_message` → an Echo announce entity. (needs someone home to listen)
- [x] Back up again (Phase A2). (verified 2026-11-28: "pre-cleanup 2026-11-28", slug 1a7aa4be, full, 109 MB)
- [ ] Tell me which IDs differ from the table, and I'll update the dashboard and the mock to match.

---

## Sources
- HA: [Matter](https://www.home-assistant.io/integrations/matter/) · [Thread](https://www.home-assistant.io/integrations/thread/) · [tado](https://www.home-assistant.io/integrations/tado/) · [HomeKit Device](https://www.home-assistant.io/integrations/homekit_controller/) · [Home Connect](https://www.home-assistant.io/integrations/home_connect/) · [Roborock](https://www.home-assistant.io/integrations/roborock/) · [vacuum.clean_area](https://www.home-assistant.io/actions/vacuum.clean_area/) · [Govee lights local](https://www.home-assistant.io/integrations/govee_light_local/) · [Alexa Devices](https://www.home-assistant.io/integrations/alexa_devices/) · [Tuya](https://www.home-assistant.io/integrations/tuya/) · [TP-Link](https://www.home-assistant.io/integrations/tplink/) · [Frontend themes](https://www.home-assistant.io/integrations/frontend/) · [2026.11 release (Marketplace)](https://www.home-assistant.io/blog/2026/11/04/release-202611/) · [2026.3 release](https://www.home-assistant.io/blog/2026/03/04/release-20263/)
- tado: [API limits](https://support.tado.com/en/articles/12165739-limitation-for-rest-api-usage) · [HomeKit reset](https://support.tado.com/en/articles/3387334-how-can-i-reset-the-homekit-configuration-of-the-internet-bridge)
- IKEA/Thread community reports: [DIRIGERA + Matter issues](https://community.home-assistant.io/t/ikea-dirigera-and-matter-integration-issues/974887) · [Thread devices not visible #160196](https://github.com/home-assistant/core/issues/160196) · [ZBT-2 vs DIRIGERA](https://community.home-assistant.io/t/zbt-2-vs-dirigera-as-thread-border-router-for-new-ikea-matter-devices-which-is-better-for-home-assistant/988607) · [DIRIGERA bridges leak/energy](https://www.matteralpha.com/news/ikea-dirigera-now-bridges-water-leak-detectors-and-power-meters-to-matter) · [ZBT-2 as Thread adapter](https://support.nabucasa.com/hc/en-us/articles/31347057208989) · [BILRESA integration](https://github.com/Vituhlos/ha-ikea-bilresa)
- Meross: [MS605 review](https://www.matteralpha.com/review/meross-ms605-review-multi-zone-presence-detection-via-matter) · [MS605 owners thread](https://community.home-assistant.io/t/meross-ms605-owners-thread/994484)
- Roborock segment cleaning: [community thread](https://community.home-assistant.io/t/roborock-integration-with-q-revo-vacuum-mop-segment-cleaning/634725)
- Others: [Govee cloud fallback](https://github.com/LaggAt/hacs-govee) · [ha_vidaatv](https://github.com/warrenrees/ha_vidaatv) · [Philips HTL3320/10](https://www.philips.co.uk/c-p/HTL3320_10/3000-series-soundbar-speaker) · [card-mod](https://github.com/thomasloven/lovelace-card-mod) · [Frosted Glass themes](https://github.com/wessamlauf/homeassistant-frosted-glass-themes)

**Not verified** (from forum reports or not checked):
- the exact IKEA app menu names
- whether DIRIGERA-shared Thread devices stay stable on your firmware
- the Q5 Pro suction strings
- humidity over HomeKit
- whether `--ha-card-backdrop-filter`-style blur works without card-mod

## Music on the Echo Dots (Music tab)
How it works (tested live 2026-11-25):
- **Now playing and controls** come from the Echo entities themselves (`media_player.echo_*`, `media_player.everywhere`): track, artist, cover, play/pause, next, stop, volume. Echo Dots have no "previous", so the dashboard asks Alexa instead.
- **Starting music** always goes through Alexa (`alexa_devices.send_text_command`), because nothing else may start playback on an Echo. Text sent to a speaker-group device is ignored, so for several rooms the dashboard sends to one member Echo and adds the group name: "play Joji on Spotify on Everywhere".
- **Everything plays on Spotify** (Free is fine), by name through Alexa. Amazon doesn't offer YouTube Music on Alexa for this account (amazon.de; the service isn't in the Alexa app's list), so the Echos can't play from YouTube Music.
- **Your YouTube Music library** (playlists, liked songs, search) comes from Music Assistant, used only as a catalogue. Tapping a song, album or artist plays the same thing on Spotify. Your own playlists play if a Spotify playlist has the same name: copy them over once (for example with tunemymusic.com). Music Assistant's generated lists (Infinite Mix, Random…) are hidden.
- Rejected: Music Assistant's experimental Alexa skill. It has no multi-room or Alexa groups, needs a separate Docker host and your own domain, and makes the Music Assistant stream public.

Setup:
1. Alexa app → More → Settings → Music & Podcasts: **Spotify** must be linked (it is).
2. HA → Settings → Apps → App store → install and start **YT Music PO Token Generator**, then **Music Assistant** (both from the Music Assistant repository, already added).
3. Open Music Assistant → Settings → Providers → Add → **YouTube Music**. Paste the cookie: in an incognito window, sign in at music.youtube.com, open the developer tools → Network, click any request to `music.youtube.com`, and copy the whole `cookie` request header. It must contain `__Secure-3PAPISID`. Leave any player providers that would stream to the Echos switched off.
4. HA → Settings → Devices & services → the discovered **Music Assistant** → Configure.
5. Optional: to play two rooms without the third, create an Alexa **speaker group** per pair (Devices → + → Combine speakers), named `Kitchen and Living Room`, `Kitchen and Studio`, `Living Room and Studio`, then reload **Alexa Devices** in HA.

**When the playlists disappear:** the YouTube cookie has expired (Music Assistant logs `401: Unauthorized` or `Unable to fetch PO Token`). Repeat step 3 with a fresh cookie. Playback and the controls keep working in the meantime.
