#!/bin/bash

# Set python path
rootPythonPath="/home/pi/py"

for dir in ${rootPythonPath}/*; do
    if [ -d $dir ]; then
        rootPythonPath="${rootPythonPath}:${dir}"
    fi
done
export PYTHONPATH="${rootPythonPath}"

sudo ${rootPythonPath}/scripts/startsoundmodem.sh &
sleep 1

sudo /${rootPythonPath}/scripts/startaxlisten.sh &
sleep 1

sleep 15 # Need to wait for soundmodem to start before main for some reason

sudo python ${rootPythonPath}/scripts/startmain.sh &
sleep 1