# Automations

**Manage them in the dashboard (v0.12.0):** the **Automations** tab ("Auto" on the iPhone) lists every automation with a plain-English summary, an on/off switch, **Run** and **Edit** (times, sunrise/sunset offsets, minutes, brightness, warmth, days, messages). **New** builds one from When / Only if / Do. Anything bigger: **HA editor** in the same sheet opens Home Assistant's full editor at that automation.

**Home Assistant is the master copy:** automations live in `/config/automations.yaml` (HA rewrites it on every save, so YAML comments don't survive). `ha/automations.yaml` is a snapshot: run `tools/pull_automations.sh` before committing. Helpers, scenes, the remote script, the robot and the vacation automations live in `ha/packages/`.

**This page matches the snapshot committed in v0.28.0.** Where this page and the YAML disagree, the YAML wins.

**Conventions**
- "Someone home" = `zone.home` above 0 (Aziz + Wifey). "Everyone left" = `zone.home` at 0.
- "Both phones" = `notify.mobile_app_azizs_iphone` and `notify.mobile_app_iphone_wifey`.
- "Echo in the occupied room" = Studio Echo if `binary_sensor.studio_presence` is on, else Kitchen Echo if `binary_sensor.kitchen_motion` or `binary_sensor.echo_kitchen_presence` is on, else the Living Room Echo (`notify.echo_studio_speak`, `notify.echo_kitchen_speak`, `notify.echo_living_room_speak`).
- "Vacation off" = `input_boolean.vacation_mode` is off. Every comfort automation below checks it unless stated otherwise.
- **Time-of-day values** = `sensor.light_mode` (`ha/packages/lighting.yaml`): morning 70 % 3000 K (05:00 to 1 h after sunrise), **day 80 % 3500 K** (until 1 h before sunset), evening 55 % 2700 K (until 22:00), night 25 % 2202 K (22:00 to 05:00).

---

## 1. Schedules

| Name (id) | Trigger | Conditions | What happens | Devices |
|---|---|---|---|---|
| **Schedule · lamps on at sunset** (`sunset_lamps`) | 30 min before sunset | Vacation off; someone home | Living-room lamp on. Studio lamp and both bedside lamps on at the time-of-day values. | `light.living_room_lamp`, `light.studio_lamp`, `light.bedside_lamps` |
| **Schedule · weekday wake-up light** (`wake_up_light`) | 20 min before `input_datetime.wake_time` (Mon-Fri) or `input_datetime.wake_time_weekend` (Sat-Sun) | Day matches the time used; `input_boolean.wake_up_enabled` on; vacation off | Bedside lamps on at 1 % / 2200 K, then fade to 80 % / 3500 K over 20 min. After the fade, the bathroom heats to 22 ° for 60 min, and the end time is written to `input_datetime.climate_timer_bathroom` so the dashboard shows the countdown. No Echo message any more. | `light.bedside_lamps`, `climate.bathroom` (tado X), `input_datetime.climate_timer_bathroom` |
| **Schedule · balcony lights on at sunset** (`balcony_lights_on`) | Sunset | Vacation off | Balcony lights on. | `light.balcony_lights` (see Known issues) |
| **Schedule · balcony lights off at 23:00** (`balcony_lights_off`) | 23:00 | none | Balcony lights off. | `light.balcony_lights` (see Known issues) |
| **Kitchen · morning weather briefing** (`morning_weather_briefing`) | Kitchen motion turns on | Vacation off; wake-up light enabled; someone home; now is between (wake time - 20 min, weekday or weekend time) and 3 h after that; not already run today | The Kitchen Echo says today's weather (condition, high, low), plus a snow warning, or an umbrella reminder when rain is expected (rainy, pouring, lightning-rainy, hail, or precipitation above 0.5 / probability 50 % or more). | `binary_sensor.kitchen_motion`, `weather.forecast_home`, `notify.echo_kitchen_speak` |

On/off and times for the wake-up light are on the dashboard (Home → Now).

## 2. Motion and presence

| Name (id) | Trigger | Conditions | What happens | Devices |
|---|---|---|---|---|
| **Kitchen · motion light** (`kitchen_motion_light`) | `binary_sensor.kitchen_motion` on | Vacation off; light not unavailable | If the ceiling is off and `sensor.kitchen_illuminance` is below 30 lx, it comes on at the time-of-day values (23:00-06:00: 10 % at 2202 K). Off 3 min after the motion stops, if it is still on. | MYGGSPRAY motion sensor, `light.kitchen_ceiling` |
| **Hallway · motion light** (`hallway_motion_light`) | `binary_sensor.hallway_motion` on | Vacation off; light not unavailable | If the light is off and `sensor.hallway_illuminance` is below 40 lx, it comes on at the time-of-day values (23:00-06:00: 10 % at 2202 K). Off 2 min after the motion stops. | MYGGSPRAY motion sensor (hallway), `light.hallway_light` |
| **Studio · lamp on when someone is there and it's dark** (`studio_presence_on`) | `binary_sensor.studio_presence` on | Vacation off; lamp off; `sensor.studio_illuminance` below 150 lx | Studio lamp on at the time-of-day values. | Meross presence sensor, `light.studio_lamp` |
| **Studio · lights off when empty for 5 min** (`studio_presence_off`) | `binary_sensor.studio_presence` off for 5 min | Vacation off | `light.studio_lights` off (5 s fade). | Meross presence sensor |
| **Studio · focus mode on desk time** (`studio_focus`) | Presence on for 2 min (`occupied`), or off for 10 min (`clear`) | `occupied`: vacation off, Mon-Fri 09:00-17:00. `clear`: none | `occupied`: Focus scene and Studio Echo do-not-disturb on. `clear`: do-not-disturb off. | `scene.focus`, `switch.echo_studio_do_not_disturb` |
| **Presence · welcome home** (`arrive_home`) | `person.muhammad_aziz_ur_rehman` or `person.wifey` changes to home (not from unknown/unavailable) | Vacation off | Waits up to 10 min for `binary_sensor.main_door` to open, then carries on even if it never opened. **Lights:** if the sun is below the horizon and the other person was not home (the flat was empty): living-room lamp on, hallway light and bedside lamps on at the time-of-day values. **Greeting:** between 07:00 and 23:00 the Kitchen Echo says "As-salaamu alaykum, Aziz" or "As-salaamu alaykum, Hatice" (Alexa's Turkish voice via SSML), for whichever person arrived. Queued, so two arrivals don't collide. | persons, `binary_sensor.main_door`, `light.living_room_lamp`, `light.hallway_light`, `light.bedside_lamps`, `notify.echo_kitchen_speak` |
| **Presence · everyone left** (`leave_home`) | `zone.home` at 0 for 5 min | none (no vacation check) | All lights off, rice cooker off, and the TV off through the living-room Echo (`alexa_devices.send_text_command`, "turn off the TV"; `continue_on_error`, so a failure never blocks the rest). | `switch.rice_cooker`, living-room Echo, Hisense TV |
| **Presence · leaving check (doors and rice cooker)** (`leaving_checks`) | `zone.home` at 0 for 2 min | Main door, balcony door or rice cooker is on | Push to both phones listing what is still open or on. | `binary_sensor.main_door`, `binary_sensor.balcony_door`, `switch.rice_cooker` |
| **Living room · heating paused while the balcony door is open** (`balcony_door_heating`) | `binary_sensor.balcony_door` on for 2 min | Living-room heating not already off | `climate.living_room` off; when the door closes, back to `auto` (the tado schedule). No vacation check. | Door sensor, tado X |
| **Bedroom · goodnight (hold bottom button)** (`goodnight_bottom_button`) | Long-press on `event.bedroom_dual_button_2` | none | Turns off living-room lights and lamp, kitchen ceiling, hallway, Studio lights, bedroom ceiling and TV lights (bedside lamps stay). Living room and Studio heating go to 17 ° until 06:30 (timer end written to `input_datetime.climate_timer_living_room` / `_studio`, shown on the dashboard countdown). Push to both phones: "Still open: ..." for an open balcony or main door, otherwise "All closed, good night." | Bedroom dual button, lights, tado X |

## 3. Remotes (`ha/automations.yaml` + `ha/packages/remotes.yaml`)

Four automations feed one script, `script.remote_light` ("Remote · light action").

**Scroll wheels** (`remote_living_room_wheel`, `remote_studio_wheel`, `remote_bedroom_wheel`; each is a BILRESA wheel with 9 event entities `event.<room>_wheel_button_1..9`). Each wheel has three channels, and each channel has up, down and press:

| Channel | Living room | Studio | Bedroom |
|---|---|---|---|
| 1 (buttons 1-3), whole room | `light.living_room_lights` | `light.studio_lights` | `light.bedroom_lights` |
| 2 (buttons 4-6), ceiling | `light.living_room_ceiling` | `light.studio_light` | `light.bedroom_ceiling` |
| 3 (buttons 7-9), lamp | `light.living_room_lamp` | `light.studio_lamp` | `light.bedside_lamps` |
| Long-press scene | `scene.movie` | `scene.focus` | `scene.night` |

- **Press** = on/off. Switching on uses the time-of-day values (on/off-only lights just switch on).
- **Turn** = dim, 5 % per click (`brightness_step_pct`). Lights that only support on/off (the living-room lamp plug) are skipped.
- **Double-tap, then turn within 10 s** = warmth. Double-tap opens a 10 s window (`input_datetime.wheel_warmth_living_room` / `_studio` / `_bedroom`); turning inside it changes colour temperature, 150 K per click, up = cooler, down = warmer, clamped to 2202-4000 K. Each turn extends the window by 10 s. If the light was off, the double-tap switches it on first.
- **Long-press** = the room's scene.

**Bedroom dual button** (`remote_bedroom_dual_button`; `event.bedroom_dual_button_1` top, `_2` bottom):
- Top, press: toggle the bedside lamps.
- Top, hold: bedside lamps on at 30 % / 2200 K.
- Bottom, press: `scene.night`.
- Bottom, hold: goodnight (see Motion and presence).

If turning feels reversed or the dual button's top/bottom are swapped, flip the marked `shortcut:` lines in `ha/packages/remotes.yaml`. For live dimming while turning, see the BILRESA integration in deploy.md B8.

## 4. Appliances

| Name (id) | Trigger | Conditions | What happens | Devices |
|---|---|---|---|---|
| **Washer · announce when finished** (`washer_done_announce`) | `sensor.washer_operation_state` becomes `finished` | none for the push; the announcement needs 08:00-22:00 and someone home | Push to both phones ("The washing machine is done."). Then the Echo in the occupied room announces it. | Siemens washer (Home Connect), both phones, Echos |
| **Washer · wet laundry reminder** (`washer_wet_laundry_reminder`) | `sensor.washer_operation_state` becomes `finished` | none up front | Waits 30 min. It is cancelled if `switch.kitchen_washing_machine_power` goes off, or the washer state leaves `finished` (a new program starts). If still pending: push to both phones, plus the Echo in the occupied room (08:00-22:00, someone home): "Laundry has been sitting in the washing machine for 30 minutes - hang it up before it gets musty." | Same, plus `switch.kitchen_washing_machine_power` |
| **Kitchen · rice cooker off after 60 min** (`rice_cooker_timeout`) | `switch.rice_cooker` on for 1 h | none | Switches it off and pushes "Switched off after 60 minutes." to both phones. | Wi-Fi plug `switch.rice_cooker` |

## 5. Air and climate

| Name (id) | Trigger | Conditions | What happens | Devices |
|---|---|---|---|---|
| **Air · fresh-air nudge when CO2 is high** (`fresh_air_nudge`) | `sensor.air_quality_co2` above 1000 ppm for 10 min, or 08:00 | Vacation off; CO2 is above 1000 ppm | Loop, once per hour, until CO2 is back at 1000 ppm or below (at most 16 rounds). Each round, if someone is home, it is 08:00-22:00 and the balcony door is closed: the Echo in the occupied room says "CO2 is at N ppm - open the balcony door for five minutes", and a push goes to whoever is home (Aziz's phone if he is home, Wifey's if she is home). | IKEA air-quality monitor, Echos, phones |

Heating timers: the wake-up light, goodnight and the dashboard's Boost all use `tado_x.set_climate_timer` and store the end time in `input_datetime.climate_timer_<room>` (`ha/packages/climate_timers.yaml`).

## 6. Robot (`ha/packages/roborock.yaml` + `ha/automations.yaml`)

Only a **finished** clean counts as "done today". A finished clean is one that ends with `sensor.studio_roborock_cleaning_progress` at 90 % or more after at least 20 min, and was not recalled.

| Name (id) | Trigger | Conditions | What happens | Devices |
|---|---|---|---|---|
| **Robot · clean when everyone is out** (`robot_clean_when_away`) | `zone.home` below 1 for 10 min | Vacation off; Mon-Sat 09:00-19:00; vacuum docked; `sensor.studio_roborock_battery` at 50 % or more; `input_datetime.robot_last_full_clean` is not today | `vacuum.start` (whole flat). | `vacuum.roborock_q5_pro` |
| **Robot · return to dock when someone comes home** (`robot_dock_on_arrival`) | `zone.home` goes above 0 | Vacuum is cleaning | Turns on `input_boolean.robot_recalled`, then `vacuum.return_to_base`. A recalled clean doesn't count, so it runs again the next time everyone is out that day. | Roborock |
| **Robot · mark full clean** (`robot_mark_full_clean`, in `roborock.yaml`) | Vacuum starts cleaning (`started`), or leaves cleaning to returning/docked (`ended`) | `ended`: `robot_recalled` off, progress 90 % or more, and the run lasted 20 min or more | `started`: clears `robot_recalled`. `ended`: stamps `input_datetime.robot_last_full_clean` with now. | Roborock, `sensor.studio_roborock_cleaning_progress` |
| **Robot · weekly maintenance check** (`robot_maintenance_weekly`) | Sundays 10:00 | At least one of main brush, side brush, filter, sensors has under 5 h left (or is overdue) | Push to both phones listing them. Silent if none. | `sensor.studio_roborock_*_time_left` |

Scripts: `script.robot_clean_selected_rooms` (rooms from `input_boolean.robot_room_*`, `input_select.robot_suction`, `input_number.robot_passes`; used by the dashboard and the vacation schedule) and `script.away` (scene button: all lights off, rice cooker off, robot starts).

## 7. Lighting rules (`ha/packages/lighting.yaml`)

| Name (id) | Trigger | Conditions | What happens |
|---|---|---|---|
| **Lights · match the time of day when turned on** (`lights_time_of_day_on_turn_on`) | One of the IKEA bulbs (kitchen 1-3, Studio lamps 1-3, `light.studio_light`, both bedside lamps, `light.bedroom_ceiling`, `light.hallway_light`, living room 1-2) goes from off/unavailable to on | The turn-on came from a person or device (not an automation), and no scene was activated in the last 5 s | Sets it to the time-of-day values (1 s fade). |
| **Lights · shift warmth when the time of day changes** (`lights_time_of_day_drift`) | `sensor.light_mode` changes | At least one of those bulbs is on in white (colour-temp) mode | Their colour temperature moves to the new mode's kelvin over 60 s. Brightness and coloured lights are left alone. |
| **Lights · bedside lamps share brightness and colour** (`bedside_lamps_mirror`) | State or attribute change on `light.bedside_lamp` or `light.bedside_lamp_2` | Changed lamp is on; change came from a person or device (prevents loops) | After 1.5 s, the other lamp copies brightness and colour (white or xy) if it is on and differs. A lamp just switched on takes the other lamp's setting. On/off stays independent. |

**Scenes** (`ha/packages/scenes.yaml`): Morning, Focus (Studio light 100 %, lamp 80 %, 4000 K), Movie (living-room ceiling lights off, lamp 20 %, `light.tv_lights` 60 %), Night (everything off except both bedside lamps at 30 % / 2200 K).

## 8. Vacation mode (`ha/packages/vacation.yaml`, `ha/packages/vacation_automations.yaml`)

Helpers: `input_boolean.vacation_mode`, `vacation_open_ended`, `vacation_security_alerts`, `vacation_preheat`, `vacation_presence_simulation`, `vacation_humidity_alerts`; `input_datetime.vacation_start`, `vacation_end`, `vacation_robot_time` (default 11:00); `input_number.vacation_robot_every_days` (default 3), `vacation_preheat_hours` (default 3). All alerts and pushes go to **both phones**.

| Name (id) | Trigger | Conditions | What happens |
|---|---|---|---|
| **Vacation · start at the scheduled time** (`vacation_start_scheduled`) | `vacation_start` reached | Vacation mode off | Turns vacation mode on. |
| **Vacation · lock the flat down** (`vacation_on`) | Vacation mode turns on | none | Stamps the real start time, all lights and the rice cooker off, all four tado rooms to `off` (frost protection), push "Vacation mode on" with the end date or "Open-ended". |
| **Vacation · keep lights and plugs off** (`vacation_keep_off`) | A listed bedroom, living-room, kitchen, Studio, TV, balcony light or the rice cooker turns on | Vacation on; not (presence simulation on, after 16:00, and the light is one of the simulation lights: living-room lamp/ceiling/lights, kitchen ceiling, bedside lamps) | Switches it straight back off. |
| **Vacation · robot cleans every N days** (`vacation_robot_schedule`) | `vacation_robot_time` | Vacation on; days since the start are above 0 and a multiple of N | If any `robot_room_*` is ticked: `script.robot_clean_selected_rooms`; otherwise a whole-flat `vacuum.start`. |
| **Vacation · security alert** (`vacation_security_alert`) | Main door, balcony door, hallway motion or kitchen motion on | Vacation on; security alerts on; robot not cleaning or returning (it sets off the motion sensors) | Time-sensitive push (breaks through Focus) to both phones: the sensor name and the time. |
| **Vacation · presence simulation** (`vacation_presence_simulation`) | Three triggers, each delayed by a random 0-20 min: sunset (`dusk`), 19:30 (`kitchen`), 22:30 (`bed`) | Vacation on; presence simulation on | `dusk`: living-room lamp on, living-room ceiling 60 % / 2700 K. `kitchen`: kitchen ceiling 70 % / 2700 K for a random 15-30 min, then off. `bed`: living-room lamp and ceiling off, bedside lamps 40 % / 2200 K. |
| **Vacation · simulation lights off for the night** (`vacation_presence_simulation_end`) | 23:15 | Vacation on | After a random 0-20 min: living-room lamp and ceiling, kitchen ceiling and bedside lamps off. |
| **Vacation · humidity alert** (`vacation_humidity_alert`) | Any of `sensor.living_room_humidity`, `studio_humidity`, `bedroom_humidity`, `bathroom_humidity` above 65 % for 2 h | Vacation on; humidity alerts on | Push to both phones (mould risk). |
| **Vacation · pre-heat before return** (`vacation_preheat`) | The end time minus N pre-heat hours is reached (template trigger) | Vacation on, not open-ended; pre-heat on | All four tado rooms back to `auto` (the tado schedule), push "Heating back on for your return." |
| **Vacation · end at the return time** (`vacation_end_scheduled`) | `vacation_end` reached | Not open-ended | Turns vacation mode off. |
| **Vacation · welcome home** (`vacation_off`) | Vacation mode on to off | none | All four tado rooms to `auto`, push "Welcome back" to both phones. |

**Test the vacation flow:**
1. Set the start to 2 min from now and the end to 10 min from now.
2. Set the pre-heat to 1 h, so it fires straight away.
3. Watch start, lock-down, pre-heat, end and welcome-back happen, and try switching a lamp on in between (keep-off).

---

## Known issues
- **Balcony lights don't exist yet.** `balcony_lights_on`, `balcony_lights_off`, `vacation_keep_off`, and the Night scene reference `light.balcony_lights`, which isn't created until the LEDVANCE plug is paired. Until then those steps have no effect on a real light.
- **The washer door sensor is unavailable.** Nothing relies on it: the wet-laundry reminder is cancelled by washer power-off (`switch.kitchen_washing_machine_power`) or a state change instead.
- **Welcome home greets even without a door opening.** After 10 min with no main-door event it carries on, so the greeting (07:00-23:00) and lights still run.
- **Everyone left** and **Balcony door heating** have no vacation check, so they still run in vacation mode.
- **Echo "announce" is silent (2026-11-28).** `notify.echo_*_announce` calls succeed but nothing plays: the Echo Announcements setting is unavailable to HA (Amazon communication-settings refreshes fail). Every automation and the dashboard use `notify.echo_*_speak` instead, which works and accepts SSML.

## Implementation notes
- `alexa_devices.send_text_command` takes `device_id` + `text_command`. TV on/off goes through it because the TV reports no state through Alexa.
- tado: HVAC mode `off` = frost protection; the cloud entity mode `auto` = back to the tado schedule. Timed heating uses `tado_x.set_climate_timer`.
- Retired from the original catalogue: tado slow refresh (tado X replaced it), movie mode on TV-on (the TV reports no state), the PM2.5 air-quality push (not chosen), and the "leaving home" robot clean inside the old leave automation (now the separate robot automations).

## Ideas, not built yet
| Idea | Why it isn't live |
|---|---|
| **Studio zones by purpose**: desk zone → task light at 4000 K; sofa zone → warm lamp only; door zone → only briefly. | Needs the zone names from you (what each of the 3 zones covers). |
| **Circadian lighting everywhere** with **Adaptive Lighting** from Marketplace (exclude the Govee strip). | The time-of-day rules above cover most of it. |
| **Echo follow-me announcements**: one script `announce_here(message)` instead of the same "occupied room" template pasted into several automations. | Washer (2), CO2 nudge and others use the template now, so it's due. |
| **TV off → lights restore** with `scene.create` snapshots. | Needs the TV integration to report reliably. |

**Needs new devices (see [`gaps.md`](gaps.md)):**
- **Bathroom**: humidity-triggered fan, a motion light, and a "shower running" warm-up. There's no bathroom light, fan or sensor yet.
- **Leak alert** under the washing machine → shut off the washer and push.
- **Energy**: washer, TV and rice-cooker power use, and "TV left on standby" alerts with energy-monitoring plugs.
- **Balcony**: a motion or lux sensor to switch the balcony lights at dusk.
- **Smart lock / doorbell**: arrival unlocks, and "who's at the door" on the Echo.
