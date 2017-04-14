#!/bin/bash

LOGPATH="/home/pi/axlisten.log"

echo "=====" >> $LOGPATH
echo "Starting axlisten: $(date)" >> $LOGPATH
echo "=====" >> $LOGPATH
axlisten &>> /home/pi/axlisten.log
