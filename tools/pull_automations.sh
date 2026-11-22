#!/bin/sh
# Home Assistant is the master copy of automations (edited from the dashboard or HA's editor).
# Run before committing so git keeps a snapshot.
scp -q -i ~/.ssh/ha_green root@192.168.178.57:/config/automations.yaml "$(dirname "$0")/../ha/automations.yaml" && echo "ha/automations.yaml updated"
