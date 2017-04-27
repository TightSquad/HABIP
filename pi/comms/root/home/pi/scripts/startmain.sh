#!/bin/bash

echo "=====" >> /home/pi/main.log
echo "Starting /home/pi/comms/main.py: $(date)" >> /home/pi/main.log
echo "=====" >> /home/pi/main.log

/home/pi/comms/main.py >> /home/pi/main.log 2>&1
