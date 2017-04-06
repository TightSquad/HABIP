"""
file: command.py
author: Connor Goldberg
project: High Altitude Balloon Instrumentation Platform
description: Abstract the command format
"""

import board
import logger

class command(object):
    """
    Base class for commands
    """

    mainCommand = {
        "CAM"       : 0x0,  # camera
        "OSD"       : 0x1,  # OSD
        "RW"        : 0x2,  # reaction wheel
        "PI"        : 0x3,  # raspberry pi
        "ATV"       : 0x4,  # analog tv
        "TIME"      : 0x5,  # time


        "CUTDOWN"   : 0xFF  # Cutdown
    }

    def __init__(self, logger, commandString, index, main):
        # The logger instance for the command
        self.logger = logger

        # The original command string
        self.commandString = commandString

        # the command index number which is acked back
        try:
            self.index = int(index)
        except Exception as e:
            self.logger("Error converting index to int: {}".format(index))
            self.index = 0

        # If the command was decoded and valid
        self.valid = False

        # the main command destination/objective identifier
        self.main = main

        # the subsequent command or destination/objective identifier
        self.sub = None

        # a board identifier for the command
        self.board = None

        # a sensor idenfifier
        self.sensor = None

    def execute(self):
        raise NotImplementedError

    @staticmethod
    def parseFromCommand(commandString, commsLogger):
        fields = commandString.split(':')

        if len(fields) < 2:
            commsLogger.log.error("Command is of an invalid length: {}".format(commandString))
        elif fields[1] not in command.mainCommand.keys():
            commsLogger.log.error("Could not find main command for: {} in command: {}".format(fields[1], commandString))
        else:
            if command.mainCommand[fields[1]] == command.mainCommand["CAM"]:
                return camCommand(commandString=commandString, fields=fields, commsLogger=commsLogger)
            elif command.mainCommand[fields[1]] == command.mainCommand["OSD"]:
                return osdCommand(commandString=commandString, fields=fields, commsLogger=commsLogger)

class camCommand(command):
    """
    Class for camera commands
    """

    subCommand = {
        "0" : 0x0,
        "1" : 0x1,
        "2" : 0x2,
        "3" : 0x3
    }

    def __init__(self, commandString, fields, commsLogger):
        # Call super constructor
        super(self.__class__, self).__init__(logger=commsLogger, commandString=commandString, index=fields[0], main=fields[1])

        if len(fields) < 3:
            commsLogger.log.error("Could not find sub command for CAM command")
        elif fields[2] not in camCommand.subCommand.keys():
            commsLogger.log.error("Found invalid sub command: {}".format(fields[2]))
        else:
            self.sub = subCommand[fields[2]]
            self.valid = True
    
    def execute(self):
        # Change the camera to the index based on the subCommand
        pass


class osdCommand(command):
    """
    Class for OSD commands
    """

    subCommand = {
        "OFF"   : 0x0, # turn off
        "ON"    : 0x1, # turn on
        "RST"   : 0x2, # power cycle
        "TEMP"  : 0x3, # change temperature sensor display
        "PRES"  : 0x4, # change pressure sensor display
        "HUM"   : 0x5, # change humidity sensor display
    }

    def __init__(self, commandString, fields, commsLogger):
        # Call super constructor
        super(self.__class__, self).__init__(logger=commsLogger, commandString=commandString, index=fields[0], main=fields[1])

        if len(fields) < 3:
            commsLogger.log.error("Could not find sub command for OSD command")
        elif fields[2] not in osdCommand.subCommand.keys():
            commsLogger.log.error("Found invalid sub command: {}".format(fields[2]))
        else:
            self.sub = osdCommand.subCommand[fields[2]]

            if self.sub < 3:
                self.valid = True
            elif len(fields) < 4:
                self.valid = False # Not enough fields in the command
            elif fields[3] not in board.board.boardID.keys():
                commsLogger.log.error("Found invalid board ID: {}".format(fields[3]))
            else:
                self.board = board.board.boardID[fields[3]]
                if self.sub == osdCommand.subCommand["HUM"]:
                    self.valid = True
                else:
                    if len(fields) < 5:
                        self.valid = False # Not enough fields in the command
                    else:
                        targetBoard = board.board.getBoard(self.board)
                        print targetBoard
                        ####### LEFT OFF HERE

        
    def execute(self):
        # Execute osd command
        pass


class reactionWheelCommand(command):
    """
    Class for reaction wheel commands
    """

    subCommand = {
        "OFF"   : 0x0, # turn off
        "ON"    : 0x1, # turn on
        "CW"    : 0x2, # turn clockwise
        "CCW"   : 0x3 # turn counter-clockwise
    }

    def __init__(self, commandString, fields, commsLogger):
        # Call super constructor
        super(self.__class__, self).__init__(logger=commsLogger, commandString=commandString, index=fields[0], main=fields[1])

    def execute(self):
        # Execute reaction wheel command
        pass


class resetCommand(command):
    """
    Class for reset commands
    """

    subCommand = board.board.boardID

    def __init__(self, commandString, fields, commsLogger):
        # Call super constructor
        super(self.__class__, self).__init__(logger=commsLogger, commandString=commandString, index=fields[0], main=fields[1])

    def execute(self):
        # Execute reset command
        pass


class atvCommand(command):
    """
    Class for ATV commands
    """

    subCommand = {
        "PWR": 0x0
    }

    def __init__(self, commandString, fields, commsLogger):
        # Call super constructor
        super(self.__class__, self).__init__(logger=commsLogger, commandString=commandString, index=fields[0], main=fields[1])

    def execute(self):
        # Execute ATV command
        pass


class cutdownCommand(command):
    """
    Class for cutdown commands
    """

    def __init__(self, commandString, fields, commsLogger):
        # Call super constructor
        super(self.__class__, self).__init__(logger=commsLogger, commandString=commandString, index=fields[0], main=fields[1])

    def execute(self):
        # Execute cutdown command
        pass


class timeCommand(command):
    """
    Class for time commands
    """

    def __init__(self, commandString, fields, commsLogger):
        # Call super constructor
        super(self.__class__, self).__init__(logger=commsLogger, commandString=commandString, index=fields[0], main=fields[1])

    def execute(self):
        # Execute time command
        pass