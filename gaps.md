# Gaps: what to add later

What the flat can't sense or control yet, ranked by value for money. Each gap lists the device type I recommend, why, and which automation it unlocks (the Tier 3 list in `automations.md`).

**Buying rules**
1. **Matter first, local only.** No device that needs its own cloud to work.
2. *(Outdated 2026-11-24: DIRIGERA removed; the Thread devices are stable through the SONOFF Dongle Max border router. New IKEA Zigbee-only gear would need a Zigbee coordinator.)* **IKEA Zigbee through DIRIGERA beats IKEA Thread** until you have a ZBT-2. Zigbee devices arrive over the stable Matter bridge; Thread devices shared from DIRIGERA are the ones that drop out (deploy.md Phase 0). After a ZBT-2, either is fine.
3. **Renter-friendly**: nothing that needs rewiring unless the landlord agrees. Bulbs, plugs, stick-on sensors and retrofit locks only.

---

## Priority 1: fix reliability first

| Gap | Recommendation | Why |
|---|---|---|
| **HA has no radio of its own** | **Home Assistant Connect ZBT-2**, used as a Thread adapter | Fixes the Thread drop-outs, lets HA update IKEA firmware, and makes every future Thread device pair straight to HA. Buy this before anything else on the list. |

## Priority 2: cheap, big everyday wins

| Gap | Recommendation | Unlocks |
|---|---|---|
| **Hallway has a motion sensor but no light** | A white-spectrum IKEA bulb in the hallway fitting | Night-path light: hallway motion → 5 % at 2200 K, 23:00–06:00. Also a welcome light when the main door opens. |
| **Bathroom has no light or motion** | IKEA bulb (check the fitting is rated for bathrooms) + an IKEA motion sensor | Motion light, dim at night; "shower running" detection with the humidity below. |
| **No leak detection** | 2× IKEA water-leak sensor (Zigbee **BADRING**): under the washer, and by the bathroom sink/toilet | Leak → washer paused through Home Connect, push to the phone, all Echos announce. Most valuable during vacation mode. |
| **TV power and soundbar volume aren't reliable** | An **IR blaster** with local HA support (e.g. Broadlink RM4 mini) behind the TV | Turns the TV on reliably (Wi-Fi wake-up is unreliable on VIDAA) and gives HA the HTL3320 soundbar's volume and input through its IR remote codes. This closes the soundbar gap in the device list. |

## Priority 3: comfort and energy

| Gap | Recommendation | Unlocks |
|---|---|---|
| **No energy monitoring** | IKEA plugs with energy metering (Zigbee **INSPELNING**) on the TV/soundbar and the rice cooker, replacing its current Wi-Fi plug | Standby power per device; "TV left on" alerts; the rice-cooker timeout can turn off when power drops (cooking done) instead of after a fixed 90 min. |
| **Whole-flat electricity use** | If your electricity meter is a digital one with an optical port: an IR reading head that HA supports locally | The Energy dashboard for the whole flat: daily use, cost, and which hours are expensive. Check the meter before buying. |
| **No blinds/curtains** | IKEA smart blinds (Zigbee, through DIRIGERA) for the bedroom; a curtain robot if you have curtains instead | Wake-up light opens the blinds too; vacation mode moves them for presence simulation; close at sunset in winter to keep heat in. |
| **Living room and bedroom have no presence** | A second **Meross MS605** for the living room; optionally one in the bedroom | Lights that stay on while you sit still (motion sensors switch off on you); Movie mode only when someone is on the sofa; "Good night" detects you're in bed. |
| **Kitchen and hallway have no temperature/humidity** | IKEA temperature/humidity sensor in the kitchen | Cooking humidity alert; better vacation humidity coverage. Low priority, since tado covers 4 rooms. |
| **Air quality alerts but nothing to act** | IKEA air purifier (Zigbee **STARKVIND**) in the living room | PM2.5 above threshold → purifier turns up automatically, quiet again when it drops; off in vacation mode. |

## Priority 4: security

| Gap | Recommendation | Unlocks |
|---|---|---|
| **No smart lock** | A retrofit lock that fits over the existing cylinder, with **Matter over Thread** (e.g. Nuki) | Unlock on arrival; "door unlocked" alerts; lock check in Leaving home and Good night; one-time access codes for a neighbour during vacation. Needs the ZBT-2. |
| **No doorbell/intercom** | Depends on the building's intercom; check its model first | "Someone at the door" on the Echos and the phone, and pause the TV. |
| **No camera** | One indoor camera with local streaming (e.g. Reolink), placed facing the main door, with a privacy mode that's on whenever you're home | Snapshot attached to the vacation security alert, so you can see whether it's a false alarm. |
| **No smart smoke alarm** | Low priority: keep your existing alarms. Matter smoke alarms are still rare. | Revisit when a local Matter/Thread model is widely available. |

## Priority 5: nice to have

| Gap | Recommendation |
|---|---|
| **No wall panel** | An old iPad or a cheap tablet on the hallway wall, running the HA Companion app in kiosk mode with the Liquid Glass dashboard. |
| **Voice depends on Amazon's cloud** | **Home Assistant Voice Preview Edition** as a local voice assistant in one room. Keep the Echos for announcements. |
| **Windows (other than the balcony door) have no sensors** | IKEA door/window sensors on the bedroom and studio windows, if tado's own open-window detection proves too slow. |

---

## No purchase needed
These sound like gaps but HA can already do them:
- **Balcony lights at dusk**: use the sun's position (`sun.sun`), already in HA. No lux sensor needed.
- **Weather**: the built-in weather integration (Met.no) for the morning briefing and "close the balcony door, rain is coming".
- **Who's home**: the Companion app on your iPhone already provides `person.aziz`.

## Shopping order (if buying in steps)
1. ZBT-2
2. Hallway bulb + bathroom bulb and motion sensor + 2 leak sensors
3. IR blaster
4. Energy plugs
5. Second presence sensor, blinds, purifier
6. Smart lock (and camera if you want vacation snapshots)

**Not checked:** current availability and prices, that the named IKEA Zigbee models (BADRING, INSPELNING, STARKVIND) are still sold where you live (if not, take IKEA's Thread equivalent after the ZBT-2), your bathroom light fitting, your electricity meter type, and your building's intercom.
