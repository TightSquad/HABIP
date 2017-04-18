#!/bin/bash

LOGPATH="/home/spex/axlisten.log"

echo "=====" >> $LOGPATH
echo "Starting axlisten: $(date)" >> $LOGPATH
echo "=====" >> $LOGPATH
sudo axlisten >> $LOGPATH 2>&1
