#!/bin/bash

# Set python path
rootPath="/home/pi"
source ${rootPath}/pythonpath.sh

sudo ${rootPath}/scripts/startsoundmodem.sh &
sleep 1

sudo /${rootPath}/scripts/startaxlisten.sh &
sleep 1

sleep 15 # Need to wait for soundmodem to start before main for some reason

sudo ${rootPath}/scripts/startmain.sh &
sleep 1
