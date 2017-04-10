"""
file: gropundComms.py
author: Connor Goldberg
project: High Altitude Balloon Instrumentation Platform
description: Abstraction for the 2m communicaions
"""

import Queue

import groundCommand
import logger

class groundComms(object):
    """
    Handle the 2m communications
    """

    def __init__(self):
        self.groundCommandQueue = Queue.Queue()

        # Create the logger
        self.logger = logger.logger("groundComms")

    def parseCommands(self, inputString):
        commandStrings = inputString.split(';')
        for commandString in [s for s in commandStrings if s]: # Loop through all non-empty command strings
            parsedCommand = groundCommand.groundCommand.parseFromString(commandString=commandString, commsLogger=self.logger)
            if parsedCommand is None or not parsedCommand.valid:
                self.logger.log.error("Could not parse command: {}".format(commandString))
            else:
                print "Parsed: {}".format(commandString)
                parsedCommand.ack()
                self.logger.log.debug("Parsed command: {}".format(commandString))
                if parsedCommand.executed is False:
                    self.groundCommandQueue.put(parsedCommand)

    def executeCommands(self):
        while not self.groundCommandQueue.empty():
            command = self.groundCommandQueue.get()
            
            try:
                command.execute()
            except Exception as e:
                self.logger.log.error("Got exception: {} trying to execute command: {}".format(e, command.commandString))
            # print command.commandString

################################# Unit Testing #################################
if __name__ == "__main__":
    c = groundComms()

    commandString = ""
    # commandString += "0001:CAM:1;0002:CAM:2;0003:CAM:3;0004:CAM:"
    # commandString += "0001:OSD:ON;0002:OSD:OFF;0003:OSD:RST;0004:OSD:HUM:B0;0005:OSD:TEMP:B5:TD0;0006:OSD:TEMP:B1:TD;"
    commandString += "0001:RW:OFF;0002:RW:ON;0003:RW:CW,90;0004:RW:CCW,90;0005:RW:CW,1000;"
    commandString += "0001:RST:B0;0002:RST:B2;0003:RST:B3;0004:RST:B8"
    # commandString += "0001:ATV:PWR,1.0;0002:ATV:PWR,5.0;0003:ATV:PWR"
    commandString += "0001:TIME:1234567890;0002:TIME:asd;"
    commandString += "0001:CUTDOWN;0002:CUTDOWN;"

    c.parseCommands(commandString)
    c.executeCommands()