#!/bin/bash

LOG_PATH="/logs/soundmodem.log"

mkdir -p /logs

echo "=====" >> $LOG_PATH
echo "Starting /home/pi/soundmodem: $(date)" >> $LOG_PATH
echo "=====" >> $LOG_PATH

/home/pi/soundmodem >> $LOG_PATH 2>&1

echo "=====" >> $LOG_PATH
echo "Closing /home/pi/soundmodem: $(date)" >> $LOG_PATH
echo "=====" >> $LOG_PATH
