#!/bin/bash

echo $(date) > /root/.bootdate

# Set python path
rootPythonPath="/home/pi/py"

for dir in ${rootPythonPath}/*; do
    if [ -d $dir ]; then
        rootPythonPath="${rootPythonPath}:${dir}"
    fi
done
export PYTHONPATH="${rootPythonPath}"

# Copy root things
cp -r /home/pi/root/* /root/

/root/startsoundmodem.sh &
sleep 1
/root/startaxlisten.sh &
