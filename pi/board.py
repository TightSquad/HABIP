"""
file: board.py
author: Connor Goldberg
project: High Altitude Balloon Instrumentation Platform
description: ID codes for the different boards and sensors
"""

class board(object):
    """
    Represent a board
    """

    boardID = {
        "B0" : 0, # Pi Hat 0
        "B1" : 1, # Pi Hat 1
        "B2" : 2, # Pi Hat 2
        "B3" : 3, # Pi Hat 3
        "B4" : 4, # DAQCS Host
        "B5" : 5  # COMMS Host
    }

    def __init__(self, number):
        self.number = number # The board id number
        self.sensors = None

    @staticmethod
    def getBoard(num):
        if num in range(0,4):
            return piHat
        elif num == board.boardID["B4"]:
            return daqcsHost
        elif num == board.boardID["B5"]:
            return commsHost
        else:
            return None

class piHat(board):
    """
    Represent a pi hat
    """

    sensors = {
        "TD0"   : None, # BCM die temp sensor
        "TB0"   : None, # Board temp 0
        "TB1"   : None, # Board temp 1
        "TE0"   : None, # External temp 0
        "TE1"   : None, # External temp 1
        "P0"    : None, # Pressure sensor 0 (basic)
        "P1"    : None, # Pressure sensor 1 (vacuum)
        "H"     : None, # Humidity
        "BV"    : None, # Battery voltage
        "BC"    : None  # Battery current
    }

    def __init__(self, num):
        super(piHat, self).__init__(num)
        

class daqcsHost(board):
    """
    Represent the daqcs host board
    """
    
    sensors = {
        "TB0"   : None, # Board temp
        "P0"    : None, # Pressure
        "V"     : None, # Supply voltage
        "C"     : None, # Supply current
        "XGY"   : None, # IMU Gyroscope X
        "YGY"   : None, # IMU Gyroscope Y
        "ZGY"   : None, # IMU Gyroscope Z
        "XAC"   : None, # IMU Acceleration X
        "YAC"   : None, # IMU Acceleration Y
        "ZAC"   : None, # IMU Acceleration Z
        "MS"    : None, # Motor controller speed
        "MC"    : None, # Motor controller current
        "MV"    : None, # Motor controller voltage
        "MD"    : None, # Motor direction
        "ME"    : None  # Motor enable/status
    }

    def __init__(self, num):
        super(daqcsHost, self).__init__(num)

class commsHost(board):
    """
    Represent the comms host board
    """

    sensors = {
        "TD0"   : None, # BCM Die temperature sensor
        "TB0"   : None, # Board temperature sensor
        "P0"    : None, # Pressure sensor - basic
        "LAT"   : None, # GPS - latitude
        "LON"   : None, # GPS - longitude
        "TM"    : None  # GPS - time
    }

    def __init__(self, num):
        super(commsHost, self).__init__(num)
