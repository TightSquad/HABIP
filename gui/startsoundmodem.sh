#!/bin/bash

LOGPATH="/home/spex/soundmodem.log"

echo "=====" >> $LOGPATH
echo "Starting soundmodem: $(date)" >> $LOGPATH
echo "=====" >> $LOGPATH

sudo soundmodem &>> $LOGPATH
