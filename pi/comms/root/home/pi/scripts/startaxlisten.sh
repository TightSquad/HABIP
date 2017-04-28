#!/bin/bash

LOG_PATH="/logs/axlisten.log"

mkdir -p /logs

echo "=====" >> $LOG_PATH
echo "Starting axlisten: $(date)" >> $LOG_PATH
echo "=====" >> $LOG_PATH

axlisten >> $LOG_PATH 2>&1

echo "=====" >> $LOG_PATH
echo "Closing axlisten: $(date)" >> $LOG_PATH
echo "=====" >> $LOG_PATH
