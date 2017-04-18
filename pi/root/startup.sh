#!/bin/bash

echo $(date) > /root/.bootdate

# Give tty group read access to the serial port
chmod 660 /dev/ttyAMA0

# Set python path
rootPythonPath="/home/pi/py"

for dir in ${rootPythonPath}/*; do
    if [ -d $dir ]; then
        rootPythonPath="${rootPythonPath}:${dir}"
    fi
done
export PYTHONPATH="${rootPythonPath}"

/root/startsoundmodem.sh &
sleep 1
/root/startaxlisten.sh &
