# cyberpower_warn
Configured scripts of cyberpower powerpanel.
This script will send email and MQTT msg when power event happens.

## Requirements
powerpanel,
mosquitto,
mosquitto-clients

## Installation
Simply `cp` all the scipts in this repo to `/etc` completes the installation.
Remember to replace `sender_email`, `sender_password` and `recipient email` in `pwrstatd-email.py`.
And `<MQTT IP>`, `<Optional, MQTT user name>` and `<Optional, MQTT user password>` in the shell scripts.

## To receive the MQTT msg
The MQTT message will be in `power/event` topic.
One can receive the message by the following script
`mosquitto_sub -h <MQTT IP> -t power/event -u <Optional, MQTT user name> -P <Optional, MQTT user password>`
