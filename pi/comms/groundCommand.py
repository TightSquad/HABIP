"""
author: Connor Goldberg
project: High Altitude Balloon Instrumentation Platform
description: Abstract the ground commands format
"""

import subprocess # To change the system time

import board
import common
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
        # [index, mainCommand, subCommand, num, sensorID]

        # The logger instance for the groundCommand
        self.logger = logger

        # The original command string
        self.commandString = commandString

        # the command index number which is acked back
        try:
            self.index = int(fields[0]) # Decode the command index as decimal
            #self.index = int(fields[0], 16) # Decode the command index as hex
        except Exception as e:
            self.logger.log.error("Error converting index to int: {}".format(fields[0]))
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

        self.params = []

        for item in fields[3:]:
            self.params.append(item)

        self.executed = False

    def __str__(self):
        return "Command: {}\nValid: {}\nExecuted: {}".format(self.commandString, self.valid, self.executed)

    def ack(self, beacon):
        ackString = "ACK:{0:04d}".format(self.index)
        self.logger.log.info("Sending ack: {}".format(ackString))
        beacon.send(ackString)

    def execute(self, interfaces):
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
    
    def execute(self, interfaces):
        # Change the camera to the index based on the subCommand
        self.logger.log.info("Executing change camera to: {}".format(self.sub))
        interfaces.cameraMux.selectCamera(camCommand.subCommand[self.sub])
        interfaces.habip_osd.update_cam_num(cam_num=camCommand.subCommand[self.sub])


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

        self.board = None
        self.sensor = None

        if self.sub is None:
            self.logger.log.error("Could not find sub command for OSD command")
        
        elif self.sub not in osdCommand.subCommand.keys():
            self.logger.log.error("Found invalid OSD sub command: {}".format(fields[2]))
        
        elif osdCommand.subCommand[self.sub] == osdCommand.subCommand["OFF"] or \
            osdCommand.subCommand[self.sub] == osdCommand.subCommand["ON"] or \
            osdCommand.subCommand[self.sub] == osdCommand.subCommand["RST"]:
                self.valid = True
        
        elif len(self.params) < 1:
            self.logger.log.error("Could not find board field in command")
        
        elif self.params[0] not in board.board.num.keys():
            self.logger.log.error("Found invalid board ID: {}".format(fields[3]))
        else:
            self.board = self.params[0]

            if osdCommand.subCommand[self.sub] == osdCommand.subCommand["HUM"]:
                    self.sensor = "H"
                    self.valid = True
            
            elif len(self.params) < 2:
                self.logger.log.error("Could not find sensor field in command")
            else:
                targetBoard = board.board.getBoard(board.board.num[self.board])
                if self.params[1] not in targetBoard.sensors:
                    self.logger.log.error("Could not find sensor: {} on board: {}".format(self.params[1], self.board))
                else:
                    self.sensor = self.params[1]
                    self.valid = True
        
    def execute(self, interfaces):
        # Execute osd command
        if osdCommand.subCommand[self.sub] == osdCommand.subCommand["OFF"]:
            # Turn off OSD
            self.logger.log.info("Command executing to turn off the OSD")
            interfaces.habip_osd.power_off()

        elif osdCommand.subCommand[self.sub] == osdCommand.subCommand["ON"]:
            # Turn on OSD
            self.logger.log.info("Command executing to turn on the OSD")
            interfaces.habip_osd.power_on()

        elif osdCommand.subCommand[self.sub] == osdCommand.subCommand["RST"]:
            # Reset OSD
            self.logger.log.info("Command executing to reset the OSD")
            interfaces.habip_osd.power_off()
            common.msleep(1000)
            interfaces.habip_osd.power_on()

        elif osdCommand.subCommand[self.sub] == osdCommand.subCommand["TEMP"]:
            # Update OSD temp sensor
            self.logger.log.info("Command executing to update the OSD temp")
            # sensorString = "{}:{}".format(self.board, self.sensor)
            # data = interfaces.boards[self.board].data[self.sensor]
            # interfaces.habip_osd.update_temp(data_source=sensorString, data_value=data)
            temperatureSensor = board.sensor(boardID=self.board, sensorID=self.sensor)
            interfaces.habip_osd.temperatureSensor = temperatureSensor

        elif osdCommand.subCommand[self.sub] == osdCommand.subCommand["PRES"]:
            # Update OSD pressure sensor
            self.logger.log.info("Command executing to update the OSD pressure")
            # sensorString = "{}:{}".format(self.board, self.sensor)
            # data = interfaces.boards[self.board].data[self.sensor]
            # interfaces.habip_osd.update_pres(data_source=sensorString, data_value=data)
            pressureSensor = board.sensor(boardID=self.board, sensorID=self.sensor)
            interfaces.habip_osd.pressureSensor = pressureSensor

        elif osdCommand.subCommand[self.sub] == osdCommand.subCommand["HUM"]:
            # Update OSD humidity sensor
            self.logger.log.info("Command executing to update the OSD humidity")
            # sensorString = "{}:H".format(self.board)
            # data = interfaces.boards[self.board].data["H"]
            # interfaces.habip_osd.update_humid(data_source=sensorString, data_value=data)
            humiditySensor = board.sensor(boardID=self.board, sensorID=self.sensor)
            interfaces.habip_osd.humiditySensor = humiditySensor


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

    def execute(self, interfaces):
        # Execute reaction wheel command
        lc = None

        if self.sub == "ON" or self.sub == "OFF":
            localCommandID = "03"
            data = '1' if self.sub == "ON" else '0'
            lc = localCommand.localCommand(logger=self.logger, commandID=localCommandID, data=data)
        else:
            localCommandID = "04"
            lc = localCommand.localCommand(logger=self.logger, commandID=localCommandID, data=[self.sub, str(self.degrees)])

        self.logger.log.info("Queueing SPI command: {}".format(lc))
        interfaces.daqcs.queueCommand(lc)


class resetCommand(groundCommand):
    """
    Class for reset commands
    """

    subCommand = board.board.num

    def __init__(self, commandString, fields, commsLogger):
        # Call super constructor
        super(self.__class__, self).__init__(logger=commsLogger, commandString=commandString, fields=fields)

        if self.sub is None:
            self.logger.log.error("Could not find sub command for RST command")
        elif self.sub not in resetCommand.subCommand.keys():
            self.logger.log.error("Found invalid RST sub command: {}".format(self.sub))
        else:
            self.valid = True

    def execute(self, interfaces):
        # Execute reset command
        localCommandID = "05"
        lc = localCommand.localCommand(logger=self.logger, commandID=localCommandID, data=self.sub)

        self.logger.log.info("Queueing SPI command: {}".format(lc))
        interfaces.daqcs.queueCommand(lc)


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
        elif self.sub not in self.subCommand.keys():
            self.logger.log.error("Found invalid ATV sub command: {}".format(self.sub))
        elif not self.params:
            self.logger.log.error("Could not find ATV power parameter")
        else:
            try:
                self.power = float(self.params[0])

                if self.power < 0.0 or self.power > 5.5:
                    self.logger.log.error("Output power out of valid range: {}".format(self.power))
                else:
                    self.valid = True
            except Exception as e:
                self.logger.log.error("Could not convert power of {} to float".format(self.params[0]))

    def execute(self, interfaces):
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

    def execute(self, interfaces):
        # Execute time command
        command = localCommand.timeCommand(logger=self.logger, secondsString=str(self.seconds))

        self.logger.log.info("Queueing SPI command: {}".format(lc))
        interfaces.daqcs.queueCommand(lc)

        # Set our local time
        cmd = ["sudo", "date", "-s", "@{}".format(self.seconds)]
        resp = subprocess.Popen(cmd)

        self.logger.log.info("Set local datetime to: {}".format(resp))


class cutdownCommand(groundCommand):
    """
    Class for cutdown commands
    """

    MIN_TIMES_SEEN = 2

    def __init__(self, commandString, fields, commsLogger):
        # Call super constructor
        super(self.__class__, self).__init__(logger=commsLogger, commandString=commandString, fields=fields)
        self.valid = True
        self.cutdownCount = 0

    def execute(self, interfaces):
        # Execute cutdown command
        self.cutdownCount += 1

        # Must see the cutdown count
        if self.cutdownCount >= cutdownCount.MIN_TIMES_SEEN:
            localCommandID = "FF"
            lc = localCommand.localCommand(logger=self.logger, commandID=localCommandID)

            self.logger.log.info("Queueing SPI command: {}".format(lc))
            interfaces.daqcs.queueCommand(lc)
