#!/bin/bash

LOG_PATH="/logs/main.log"

mkdir -p /logs

echo "=====" >> $LOG_PATH
echo "Starting /home/pi/comms/main.py: $(date)" >> $LOG_PATH
echo "=====" >> $LOG_PATH

python /home/pi/comms/main.py >> $LOG_PATH 2>&1

echo "=====" >> $LOG_PATH
echo "Closing /home/pi/comms/main.py: $(date)" >> $LOG_PATH
echo "=====" >> $LOG_PATH
