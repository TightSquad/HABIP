"""
author: Connor Goldberg
project: High Altitude Balloon Instrumentation Platform
description: Abstraction for the 2m communicaions
"""

import groundCommand
import logger

class groundComms(object):
    """
    Handle the 2m communications
    """

    def __init__(self):
        self.groundCommandList = []

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
                    self.groundCommandList.insert(0, parsedCommand)


    def executeCommands(self):
        while self.groundCommandList:
            command = self.groundCommandList.pop()
            
            try:
                command.execute()
            except Exception as e:
                self.logger.log.error("Got exception: {} trying to execute command: {}".format(e, command.commandString))
            
            self.logger.log.info("Executed command: {}".format(command.commandString))
