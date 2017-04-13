#!/usr/bin/env python

import axreader
import common
import groundComms

################################# Unit Testing #################################
if __name__ == "__main__":

    LOG_PATH = "ax.log"
    AX_INTERFACES = ["sm0"]
    AX_SOURCES = ["W2RIT"]
    AX_DESTINATIONS = [] #["W2RIT-10"]

    c = groundComms.groundComms()
    reader = axreader.axreader(filePath=LOG_PATH, interfaces=AX_INTERFACES, sources=AX_SOURCES, destinations=AX_DESTINATIONS)

    # while False:
    while True:
        # Get packets from axreader
        packets = reader.getNewData()

        if packets:
            for packet in packets:
                print packet
                print "--------"

                # Parse the commands
                c.parseCommands(packet.data)

        if c.groundCommandList:
            for item in c.groundCommandList:
                print item
                print "---"

        # Execute the commands
        c.executeCommands()

        # Sleep a bit
        common.msleep(1000)

    commandString = ""
    # commandString += "0001:CAM:1;0002:CAM:2;0003:CAM:3;"
    # commandString += "0001:OSD:ON;0002:OSD:OFF;0003:OSD:RST;0004:OSD:HUM:B0;0005:OSD:TEMP:B5:TD0;0006:OSD:TEMP:B1:TD;"
    # commandString += "0001:RW:OFF;0002:RW:ON;0003:RW:CW,90;0004:RW:CCW,90;0005:RW:CW,1000;"
    # commandString += "0001:RST:B0;0002:RST:B2;0003:RST:B3;0004:RST:B8"
    # commandString += "0001:ATV:PWR:1.0;0002:ATV:PWR:5.5;0003:ATV:PWR"
    # commandString += "0001:TIME:1234567890;0002:TIME:asd;"
    # commandString += "0001:CUTDOWN;0002:CUTDOWN;"

    # c.parseCommands(commandString)
    # c.executeCommands()