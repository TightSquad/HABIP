#!/bin/bash

#!/bin/bash

LOGPATH="/home/pi/soundmodem.log"

echo "=====" >> $LOGPATH
echo "Starting /home/pi/soundmodem: $(date)" >> $LOGPATH
echo "=====" >> $LOGPATH

/home/pi/soundmodem &>> $LOGPATH
