"""
file: groundCommand.py
author: Connor Goldberg
project: High Altitude Balloon Instrumentation Platform
description: Abstract the ground commands format
"""

import board
import localCommand

class groundCommand(object):
    """
    Base class for ground commands
    """

    # Used as an enum, make sure each key has a unique value
    mainCommand = {
        "CAM"       : 0x0,  # camera
        "OSD"       : 0x1,  # OSD
        "RW"        : 0x2,  # reaction wheel
        "RST"       : 0x3,  # raspberry pi
        "ATV"       : 0x4,  # analog tv
        "TIME"      : 0x5,  # time

        "CUTDOWN"   : 0xFF  # Cutdown
    }

    def __init__(self, logger, commandString, fields):
        
        # Fields follows the following format:
        # [index, mainCommand, subCommand, boardID, sensorID]

        # The logger instance for the groundCommand
        self.logger = logger

        # The original command string
        self.commandString = commandString

        # the command index number which is acked back
        try:
            self.index = int(fields[0])
        except Exception as e:
            self.logger("Error converting index to int: {}".format(fields[0]))
            self.index = 0

        # If the command was decoded and valid
        self.valid = False

        # the main command destination/objective identifier
        self.main = fields[1]

        # the subsequent command or destination/objective identifier
        if len(fields) > 2:
            self.sub = fields[2]
        else:
            self.sub = None

        # a board identifier for the command
        if len(fields) > 3:
            self.board = fields[3]
        else:
            self.board = None

        # a sensor idenfifier
        if len(fields) > 4:
            self.sensor = fields[4]
        else:
            self.sensor = None

        self.executed = False

    def ack(self):
        print "ACK:{0:04d}".format(self.index)

    def execute(self):
        raise NotImplementedError

    @staticmethod
    def parseFromString(commandString, commsLogger):
        """
        Returns a parsed command object based on the command string input
        """
        fields = commandString.split(':')

        if len(fields) < 2:
            commsLogger.log.error("Command is of an invalid length: {}".format(commandString))
            return None
        elif fields[1] not in groundCommand.mainCommand.keys():
            commsLogger.log.error("Could not find main command for: {} in command: {}".format(fields[1], commandString))
            return None
        else:
            if groundCommand.mainCommand[fields[1]] == groundCommand.mainCommand["CAM"]:
                return camCommand(commandString=commandString, fields=fields, commsLogger=commsLogger)
            elif groundCommand.mainCommand[fields[1]] == groundCommand.mainCommand["OSD"]:
                return osdCommand(commandString=commandString, fields=fields, commsLogger=commsLogger)
            elif groundCommand.mainCommand[fields[1]] == groundCommand.mainCommand["RW"]:
                return reactionWheelCommand(commandString=commandString, fields=fields, commsLogger=commsLogger)
            elif groundCommand.mainCommand[fields[1]] == groundCommand.mainCommand["RST"]:
                return resetCommand(commandString=commandString, fields=fields, commsLogger=commsLogger)
            elif groundCommand.mainCommand[fields[1]] == groundCommand.mainCommand["ATV"]:
                return atvCommand(commandString=commandString, fields=fields, commsLogger=commsLogger)
            elif groundCommand.mainCommand[fields[1]] == groundCommand.mainCommand["TIME"]:
                return timeCommand(commandString=commandString, fields=fields, commsLogger=commsLogger)
            elif groundCommand.mainCommand[fields[1]] == groundCommand.mainCommand["CUTDOWN"]:
                return cutdownCommand(commandString=commandString, fields=fields, commsLogger=commsLogger)
            else:
                commsLogger.log.error("Did not implement class for {} command".format(fields[1]))
                return None

class camCommand(groundCommand):
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
        super(self.__class__, self).__init__(logger=commsLogger, commandString=commandString, fields=fields)

        if self.sub is None:
            self.logger.log.error("Could not find sub command for CAM command")
        elif self.sub not in camCommand.subCommand.keys():
            self.logger.log.error("Found invalid sub command: {}".format(fields[2]))
        else:
            self.valid = True
    
    def execute(self):
        # Change the camera to the index based on the subCommand
        pass


class osdCommand(groundCommand):
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
        super(self.__class__, self).__init__(logger=commsLogger, commandString=commandString, fields=fields)

        if self.sub is None:
            self.logger.log.error("Could not find sub command for OSD command")
        
        elif self.sub not in osdCommand.subCommand.keys():
            self.logger.log.error("Found invalid OSD sub command: {}".format(fields[2]))
        
        elif osdCommand.subCommand[self.sub] == osdCommand.subCommand["OFF"] or \
            osdCommand.subCommand[self.sub] == osdCommand.subCommand["ON"] or \
            osdCommand.subCommand[self.sub] == osdCommand.subCommand["RST"]:
                self.valid = True
        
        elif self.board is None:
            self.logger.log.error("Could not find board field in command")
        
        elif self.board not in board.board.boardID.keys():
            self.logger.log.error("Found invalid board ID: {}".format(fields[3]))
            
        elif osdCommand.subCommand[self.sub] == osdCommand.subCommand["HUM"]:
                self.valid = True
        
        elif self.sensor is None:
            self.logger.log.error("Could not find sensor field in command")
        else:
            targetBoard = board.board.getBoard(board.board.boardID[self.board])
            if self.sensor not in targetBoard.sensors.keys():
                self.logger.log.error("Could not find sensor: {} on board: {}".format(self.sensor, self.board))
            else:
                self.valid = True
        
    def execute(self):
        # Execute osd command
        pass


class reactionWheelCommand(groundCommand):
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
        super(self.__class__, self).__init__(logger=commsLogger, commandString=commandString, fields=fields)

        # Degrees of rotation
        self.degrees = None

        if self.sub is None:
            self.logger.log.error("Could not find sub command for RW command")
        elif self.sub == "ON" or self.sub == "OFF":
            self.valid = True
        elif not self.sub.startswith("CW") and not self.sub.startswith("CCW"):
            self.logger.log.error("Found invalid RW sub command: {}".format(self.sub))
        else:
            split = self.sub.split(",")
            if len(split) != 2:
                self.logger.log.error("Found invalid RW sub command: {}".format(self.sub))
            else:
                self.sub = split[0]

                try:
                    self.degrees = int(split[1])
                    if self.degrees < 0 or self.degrees > 180:
                        self.logger.log.error("Degrees out of valid range: {}".format(self.degrees))
                    else:
                        self.valid = True
                except Exception as e:
                    self.logger.log.error("Could not convert {} to degrees".format(split[1]))


    def execute(self):
        # Execute reaction wheel command

        if self.sub == "ON" or self.sub == "OFF":
            localCommandID = "03"
            data = '1' if self.sub == "ON" else '0'
            lc = localCommand.localCommand(logger=self.logger, commandID=localCommandID, data=data)
            print lc
        else:
            localCommandID = "04"
            lc = localCommand.localCommand(logger=self.logger, commandID=localCommandID, data=[self.sub, str(self.degrees)])
            print lc

        self.logger.log.info("Executing command: {}".format(lc))

class resetCommand(groundCommand):
    """
    Class for reset commands
    """

    subCommand = board.board.boardID

    def __init__(self, commandString, fields, commsLogger):
        # Call super constructor
        super(self.__class__, self).__init__(logger=commsLogger, commandString=commandString, fields=fields)

        if self.sub is None:
            self.logger.log.error("Could not find sub command for RST command")
        elif self.sub not in resetCommand.subCommand.keys():
            self.logger.log.error("Found invalid RST sub command: {}".format(self.sub))
        else:
            self.valid = True

    def execute(self):
        # Execute reset command
        localCommandID = "05"
        lc = localCommand.localCommand(logger=self.logger, commandID=localCommandID, data=self.sub)
        print lc

        self.logger.log.info("Executing command: {}".format(lc))

class atvCommand(groundCommand):
    """
    Class for ATV commands
    """

    subCommand = {
        "PWR": 0x0
    }

    def __init__(self, commandString, fields, commsLogger):
        # Call super constructor
        super(self.__class__, self).__init__(logger=commsLogger, commandString=commandString, fields=fields)

        self.power = None

        if self.sub is None:
            self.logger.log.error("Could not find sub command for ATV command")
        elif not self.sub.startswith("PWR"):
            self.logger.log.error("Found invalid ATV sub command: {}".format(self.sub))
        else:
            split = self.sub.split(',')
            if len(split) != 2:
                self.logger.log.error("Found invalid ATV sub command: {}".format(self.sub))
            else:
                self.sub = split[0]

                try:
                    self.power = float(split[1])

                    if self.power < 0.0 or self.power > 5.5:
                        self.logger.log.error("Output power out of valid range: {}".format(self.power))
                    else:
                        self.valid = True
                except Exception as e:
                    self.logger.log.error("Could not convert power of {} to float".format(split[1]))

    def execute(self):
        # Execute ATV command
        pass


class timeCommand(groundCommand):
    """
    Class for time commands
    """

    def __init__(self, commandString, fields, commsLogger):
        # Call super constructor
        super(self.__class__, self).__init__(logger=commsLogger, commandString=commandString, fields=fields)

        self.seconds = None

        if self.sub is None:
            self.logger.log.error("Could not find valid time parameter")
        else:
            try:
                self.seconds = int(self.sub)
                self.valid = True
            except Exception as e:
                self.logger.log.error("Could not convert time to an int: {}".format(self.sub))

    def execute(self):
        # Execute time command
        localCommandID = "06"
        lc = localCommand.localCommand(logger=self.logger, commandID=localCommandID, data=str(self.seconds))
        print lc

        self.logger.log.info("Executing command: {}".format(lc))


class cutdownCommand(groundCommand):
    """
    Class for cutdown commands
    """

    def __init__(self, commandString, fields, commsLogger):
        # Call super constructor
        super(self.__class__, self).__init__(logger=commsLogger, commandString=commandString, fields=fields)
        self.valid = True

    def execute(self):
        # Execute cutdown command
        localCommandID = "FF"
        lc = localCommand.localCommand(logger=self.logger, commandID=localCommandID)
        print lc

        self.logger.log.info("Executing command: {}".format(lc))
