#!/bin/bash

echo "=====" >> /home/pi/axlisten.log
echo "Starting axlisten: $(date)" >> /home/pi/axlisten.log
echo "=====" >> /home/pi/axlisten.log

axlisten >> /home/pi/axlisten.log 2>&1
