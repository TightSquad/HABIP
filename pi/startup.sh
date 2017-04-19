#!/bin/bash

# Change permissions to the uart
sudo chmod a+rw /dev/ttyAMA0

# Set python path
rootPythonPath="/home/pi/py"

for dir in ${rootPythonPath}/*; do
    if [ -d $dir ]; then
        rootPythonPath="${rootPythonPath}:${dir}"
    fi
done
export PYTHONPATH="${rootPythonPath}"

sudo /home/pi/py/scripts/startsoundmodem.sh &
sleep 1

sudo /home/pi/py/scripts/startaxlisten.sh &
sleep 1

sleep 15 # Need to wait for soundmodem to start before main for some reason

sudo python /home/pi/py/comms/main.py &
sleep 1
