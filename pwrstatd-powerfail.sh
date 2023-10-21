#!/bin/bash

EVENT="powerfail"
WARNING="Warning: Utility power failure has occurred for a while, system will be shutdown soon!"
echo ${WARNING} | wall

MQTT_HOST="<MQTT IP>"
MQTT_USER="<Optional, MQTT user name>"
MQTT_PW="<Optional, MQTT user password>"

mosquitto_pub -h ${MQTT_HOST} -t power/event -m ${EVENT} -u ${MQTT_USER} -P ${MQTT_PW}
python3 /etc/pwrstatd-email.py ${EVENT} ${WARNING}
