#!/bin/bash

# Set python path
rootPath="/home/pi/py"
rootPythonPath="$rootPath"

for dir in ${rootPythonPath}/*; do
    if [ -d $dir ]; then
        rootPythonPath="${rootPythonPath}:${dir}"
    fi
done
export PYTHONPATH="${rootPythonPath}"

sudo ${rootPath}/scripts/startsoundmodem.sh &
sleep 1

sudo /${rootPath}/scripts/startaxlisten.sh &
sleep 1

sleep 15 # Need to wait for soundmodem to start before main for some reason

sudo ${rootPath}/scripts/startmain.sh &
sleep 1
