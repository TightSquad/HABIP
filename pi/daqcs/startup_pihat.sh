#!/bin/bash

# Change permissions to the uart
sudo chmod a+rw /dev/ttyAMA0

# Set python path
rootPythonPath="/home/pi/habip/sensors_sw/classes"

for dir in ${rootPythonPath}/*; do
    if [ -d $dir ]; then
        rootPythonPath="${rootPythonPath}:${dir}"
    fi
done
export PYTHONPATH="${rootPythonPath}"

sudo nohup python /home/pi/habip/sensors_sw/log_i2c_pihat_sensors.py &
sleep 1

sudo nohup python /home/pi/habip/sensors_sw/log_w1_pihat_sensors.py &
sleep 1

sudo nohup python /home/pi/habip/photo_video_sw/log_photo_video.py &
sleep 1

#sudo nohup python /home/pi/habip/uart_monitor/uart_monitor.py &
#sleep 1