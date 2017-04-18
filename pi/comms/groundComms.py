"""
author: Connor Goldberg
project: High Altitude Balloon Instrumentation Platform
description: Abstraction for the 2m communicaions
"""

import axreader
import common
import groundCommand
import logger

class groundComms(object):
    """
    Handle the 2m communications
    """

    def __init__(self, axLogPath, interfaces):
        self.groundCommandList = []

        # Create the logger
        self.logger = logger.logger("groundComms")

        self.interfaces = interfaces

        AX_INTERFACES = ["sm0"]
        AX_SOURCES = ["W2RIT"]
        AX_DESTINATIONS = ["W2RIT-11"]

        self.reader = axreader.axreader(filePath=axLogPath, interfaces=AX_INTERFACES, sources=AX_SOURCES, destinations=AX_DESTINATIONS)


    def update(self):
        # Check the axlog for new packets
        packets = self.reader.getNewData()

        for packet in packets:
            self.parseCommands(packet.data)


    def parseCommands(self, inputString):
        commandStrings = inputString.split(';')
        for commandString in [s for s in commandStrings if s]: # Loop through all non-empty command strings
            parsedCommand = groundCommand.groundCommand.parseFromString(commandString=commandString, commsLogger=self.logger)
            if parsedCommand is None or not parsedCommand.valid:
                self.logger.log.error("Could not parse command: {}".format(commandString))
            else:
                parsedCommand.ack(beacon=self.interfaces.beacon)
                self.logger.log.debug("Parsed command: {}".format(commandString))
                if parsedCommand.executed is False:
                    self.groundCommandList.insert(0, parsedCommand)


    def executeCommands(self, withDelay=None):
        while self.groundCommandList:
            command = self.groundCommandList.pop()
            
            try:
                command.execute(interfaces=self.interfaces)
                if withDelay:
                    common.msleep(withDelay)
            except Exception as e:
                self.logger.log.error("Got exception: {} trying to execute command: {}".format(e, command.commandString))
            
            self.logger.log.info("Executed command: {}".format(command.commandString))
