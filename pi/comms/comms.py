"""
file: comms.py
author: Connor Goldberg
project: High Altitude Balloon Instrumentation Platform
description: Abstraction for the 2m communicaions
"""

import command
import logger

class comms(object):
    """
    Handle the 2m communications
    """

    def __init__(self):
        self.commandQueue = []

        # Create the logger
        self.logger = logger.logger("comms")

    def parseCommands(self, inputString):
        commandStrings = inputString.split(';')
        for commandString in [s for s in commandStrings if s]: # Loop through all non-empty command strings
            parsedCommand = command.command.parseFromCommand(commandString=commandString, commsLogger=self.logger)
            if parsedCommand is None or not parsedCommand.valid:
                self.logger.log.error("Could not parse command: {}".format(commandString))
            else:
                print parsedCommand.index


################################# Unit Testing #################################
if __name__ == "__main__":
    c = comms()


    # commandString = "0001:CAM:1;0002:CAM:2;0003:CAM:3"
    commandString = "0001:OSD:ON;0002:OSD:OFF;0003:OSD:RST;0004:OSD:HUM:B0;0005:OSD:TEMP:B5:TB0;"
    c.parseCommands(commandString)