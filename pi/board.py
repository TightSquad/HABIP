"""
author: Connor Goldberg
project: High Altitude Balloon Instrumentation Platform
description: Structures to store the sensor IDs and values
"""

class sensor(object):
    """
    Holds a sensor's location
    """

    def __init__(self, boardID, sensorID):
        self.boardID = boardID
        self.sensorID = sensorID

    def __str__(self):
        return "{}:{}".format(self.boardID, self.sensorID)

class board(object):
    """
    Represent a board
    """

    num = {
        "B0" : 0, # Pi Hat 0
        "B1" : 1, # Pi Hat 1
        "B2" : 2, # Pi Hat 2
        "B3" : 3, # Pi Hat 3
        "B4" : 4, # DAQCS Host
        "B5" : 5  # COMMS Host
    }

    sensors = None

    def __init__(self, number):
        self.number = number # The board id number
        
        # Initialize the sensor data
        self.data = {}
        for sensor in self.sensors:
            self.data[sensor] = None

    def printAllData(self):
        s = ""
        for sensor in self.sensors:
            s += "{}: {}".format(sensor, self.data[sensor])

    @staticmethod
    def getBoard(num):
        if num in range(0,4):
            return piHat(num=num)
        elif num == board.num["B4"]:
            return daqcsHost(num=num)
        elif num == board.num["B5"]:
            return commsHost(num=num)
        else:
            return None

class piHat(board):
    """
    Represent a pi hat
    """

    sensors = [
        "TD0",  # BCM die temp sensor
        "TB0",  # Board temp 0
        "TB1",  # Board temp 1
        "TE0",  # External temp 0
        "TE1",  # External temp 1
        "P0",   # Pressure sensor 0 (basic)
        "P1",   # Pressure sensor 1 (vacuum)
        "H",    # Humidity
        "V",    # Battery voltage
        "C",    # Battery current
    ]

    def __init__(self, num):
        super(piHat, self).__init__(num)

class daqcsHost(board):
    """
    Represent the daqcs host board
    """
    
    sensors = [
        "TB0",  # Board temp
        "P0",   # Pressure
        "PB",   # Pressure
        "V",    # Supply voltage
        "C",    # Supply current
        "XGY",  # IMU Gyroscope X
        "YGY",  # IMU Gyroscope Y
        "ZGY",  # IMU Gyroscope Z
        "XAC",  # IMU Acceleration X
        "YAC",  # IMU Acceleration Y
        "ZAC",  # IMU Acceleration Z
        "MS",   # Motor controller speed
        "MC",   # Motor controller current
        "MV",   # Motor controller voltage
        "MD",   # Motor direction
        "ME",    # Motor enable/status
    ]

    def __init__(self, num):
        super(daqcsHost, self).__init__(num)

class commsHost(board):
    """
    Represent the comms host board
    """

    sensors = [
        "TD0",  # BCM Die temperature sensor
        "TB0",  # Board temperature sensor
        "P0",   # Pressure sensor - basic
        "LAT",  # GPS - latitude
        "LON",  # GPS - longitude
        "TM",   # GPS - time
        "SPD",  # GPS - speed
        "ALT",  # GPS - altitude
    ]

    def __init__(self, num):
        super(commsHost, self).__init__(num)
