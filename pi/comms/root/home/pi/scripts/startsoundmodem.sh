#!/bin/bash

echo "=====" >> /home/pi/soundmodem.log
echo "Starting /home/pi/soundmodem: $(date)" >> /home/pi/soundmodem.log
echo "=====" >> /home/pi/soundmodem.log

/home/pi/soundmodem >> /home/pi/soundmodem.log 2>&1
