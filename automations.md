# Automations

There are three tiers:
- **Tier 1** is written and ready to install: `ha/packages/automations.yaml` (everyday) and `ha/packages/vacation_automations.yaml`.
- **Tier 2** is the next round, once devices are paired and we know their real event names.
- **Tier 3** needs devices you don't have yet (see `gaps.md`, next step).

**One rule for all of them:** every comfort automation has the condition *vacation mode is off*. Vacation mode pauses them without disabling anything, so nothing can be forgotten "off" after a trip.

## Before installing: replace 3 placeholders
| Placeholder | Where to find yours |
|---|---|
| `notify.mobile_app_aziz_iphone` | Tools → Actions → type "mobile_app": your iPhone's notify action |
| `person.aziz` | Settings → People: your person entity (the Companion app provides location) |
| `REPLACE_WITH_…_ECHO_DEVICE_ID` (wake-up light) | Settings → Devices → the Echo → the device ID in the URL |

The packages load from `/config/packages/` (deploy.md Phase A7). After copying: Tools → YAML → *Check configuration*, then *Automations* reload.

---

## Tier 1: everyday (ready)

| # | Automation | What happens | Devices | Test |
|---|---|---|---|---|
| 1 | **tado slow refresh** | Every 30 min, the tado cloud entities update once. That's about 48 calls a day, under the free 100. Needed because polling is off (deploy C1). | tado cloud | Tools → States: `climate.*_tado` last-updated moves every 30 min |
| 2 | **Studio presence light** | Any Meross zone occupied **and** below 150 lux → Studio Lamp on. Warmth follows the time of day: 4000 K daytime, 3000 K evening, 2200 K late. | Meross MS605 (zones + lux), Studio Lamp | Walk in with the room dim; then cover the sensor's light window |
| 3 | **Studio empty → off** | All three zones clear for 5 min → both Studio lights fade off. | Meross, Studio lights | Leave the room and wait 5 min |
| 4 | **Kitchen motion light** | Motion → ceiling on: 100% 4000 K by day, **15% 2200 K at night**. Off 3 min after the motion stops. | MYGGSPRAY, kitchen ceiling | Wave at the sensor at 23:30 |
| 5 | **Washer done** | The "program finished" event → an Echo **in the room you're in** announces it (presence decides Studio / Kitchen / Living room). Only 08:00–22:00 and when you're home. A phone push always goes out. | Home Connect, Meross, MYGGSPRAY, Echo Dots | Run a short program |
| 6 | **Balcony door → heating pause** | Door open 2 min → living-room tado off. Closed → heating back on. | Door sensor, tado (HomeKit) | Open the balcony door for 2 min |
| 7 | **Rice-cooker timeout** | Plug on for 90 min → off, plus a push. A safety net for forgotten cookers. | Wi-Fi plug | Set `for:` to 1 min temporarily |
| 8 | **Leaving home** | Phone leaves home for 5 min → all lights off, plug off, a push **if a door is open**, and the robot cleans your selected rooms (if it hasn't run in 20 h). | Phone, lights, doors, Roborock | Tools → States: set `person.aziz` to `not_home` |
| 9 | **Welcome home** | Main door opens within 10 min of you arriving, after dark, with every light off → living room 70% at 2700 K, and the robot docks if it's still cleaning. | Door sensor, phone, ceiling lights, Roborock | Arrive after sunset |
| 10 | **Weekday wake-up light** | 20 min before your wake time, the bedside lamp rises from 1% at 2200 K to 80% at 3500 K. At wake time the bathroom heats to 22° and the Echo says "good morning" (your Alexa briefing). On/off and time are on the dashboard. | Bedside lamp, tado, Echo | Set the wake time 21 min ahead |
| 11 | **Movie mode** | TV turns on after dark → *Movie* scene: ceiling off, lamp 20%, Govee strip on. | Hisense TV, lights, Govee | Turn the TV on in the evening |
| 12 | **Air-quality alert** | PM2.5 above 25 µg/m³ for 10 min → push "air the room". Starts working once the IKEA monitor is back online. | IKEA air-quality monitor | Tools → States: set the PM2.5 sensor to 30 |

## Tier 1: vacation mode (ready)

| # | Automation | What happens |
|---|---|---|
| V1 | **Scheduled start** | At the start date/time, vacation mode switches on. |
| V2 | **Lock-down** | When it turns on: all lights and the plug go off, tado goes to frost protection, and a push confirms the end date (or "open-ended"). |
| V3 | **Keep off** | Any light or the plug turned on → switched straight back off. Exception: the 2 presence-simulation lamps in the evening. |
| V4 | **Robot schedule** | At the robot time, every N days after the start, it cleans your selected rooms (or the whole flat if none are ticked). |
| V5 | **Security alert** | A door opens or motion is seen → a **time-sensitive push** that breaks through Focus modes. Ignored while the robot is cleaning, since it sets off the motion sensors. |
| V6 | **Presence simulation** | After dark, 18:00–23:00, every ~20 min (with a random delay) the living room lamp or bedside lamp toggles. Everything is off at 23:15. |
| V7 | **Humidity alert** | Any room above 65% for 2 h → push (mould risk). |
| V8 | **Pre-heat** | N hours before the return time, tado goes back to your normal schedule. |
| V9 | **Scheduled end** | At the return time, vacation mode switches off (open-ended stays on until you end it). |
| V10 | **Welcome back** | When it turns off: tado back to schedule, plus a "Welcome back" push. |

**Test the vacation flow:**
1. Set the start to 2 min from now and the end to 10 min from now.
2. Set the pre-heat to 1 h, so it fires straight away.
3. Watch V1 → V2 → V8 → V9 → V10 happen, and try switching a lamp on in between (V3).

---

## Tier 2: next round (after pairing)

| Idea | Why it's not in Tier 1 yet |
|---|---|
| **BILRESA scroll wheels as dimmers**: turning dims the room's lights live; press toggles; double press cycles scenes (Living → Movie, Bedroom → Night, Studio → Focus). The bedroom dual button: top = bedside lamps, bottom = *Good night*. | Needs the real event names after pairing, and ideally the BILRESA integration for live turning (deploy B8). |
| **Studio zones by purpose**: desk zone → task light at 4000 K; sofa zone → warm lamp only; door zone → only briefly. | Needs the zone names from you (what each of the 3 zones covers). |
| **Circadian lighting everywhere**: every IKEA light follows the sun's warmth through the day. | Best done with **Adaptive Lighting** from Marketplace rather than hand-written rules. Install it after pairing and exclude the Govee strip. |
| **Good night** (one tap or the BILRESA bottom button): everything off except the bedside lamp at 10%, then a check that doors are closed, the rice cooker is off and the robot is docked, spoken by the bedroom Echo only if something's wrong. | Needs the button events. |
| **Laundry left in the drum**: washer finished but door not opened within 45 min → a second reminder. | Needs to confirm that the Home Connect door sensor updates after the program ends. |
| **Robot when nobody's home**: on weekdays, if you leave between 08:00 and 17:00 and the last clean was more than 2 days ago → clean everything at Turbo. | Tune once there's real history. |
| **Echo follow-me announcements**: a script `announce_here(message)` used by every automation, picking the Echo in the occupied room. | Generalises #5. Worth doing once 3+ automations announce things. |
| **TV off → lights restore**: when the TV turns off, bring back whatever the lights were before Movie mode. | Use `scene.create` snapshots; needs the TV integration to report reliably. |

## Tier 3: needs new devices (see `gaps.md`)
- **Hallway night-path light**: the hallway has a motion sensor but **no light**.
- **Bathroom**: humidity-triggered fan, a motion light, and a "shower running" warm-up. There's no bathroom light, fan or sensor yet.
- **Leak alert** under the washing machine → shut off the washer and push.
- **Energy**: washer, TV and rice-cooker power use, and "TV left on standby" alerts with energy-monitoring plugs.
- **Balcony**: a motion or lux sensor to switch the balcony lights at dusk.
- **Smart lock / doorbell**: arrival unlocks, and "who's at the door" on the Echo.

---

## Verified vs assumed
- **Checked:** the YAML parses, every condition is well-formed, the automation IDs are unique, and every comfort automation checks vacation mode.
- **Assumed:**
  - entity IDs follow the deploy.md Phase D table
  - the tado cloud humidity sensors are named `sensor.<room>_humidity`
  - `alexa_devices.send_text_command` takes `device_id` + `text_command`
  - setting tado to HomeKit `off` = frost protection, and the cloud entity `auto` = back to the tado schedule
  - Check all of these against your real entities after pairing.
