#!/usr/bin/env python

import axreader
import common
import groundComms
import time
import logging

if __name__ == "__main__":

    LOG_IN_PATH = "/home/spex/axlisten.log"
    LOG_DATA_PATH = "/home/spex/habip_data.log"
    LOG_CMDACK_PATH = "/home/spex/habip_ack.log"
    AX_INTERFACES = ["sm0"]
    AX_SOURCES = ["W2RIT-11"]
    AX_DESTINATIONS = ["W2RIT"]

    # Axlisten parser
    reader = axreader.axreader(filePath=LOG_IN_PATH, interfaces=AX_INTERFACES, sources=AX_SOURCES, destinations=AX_DESTINATIONS)

    # HABIP Data logger
    dataLogger = logging.getLogger("datalog")
    dataLoggerHandler = logging.FileHandler(LOG_DATA_PATH)
    dataLoggerFormatter = logging.Formatter("%(asctime)s,%(message)s",datefmt="%H:%M:%S")
    dataLoggerHandler.setFormatter(dataLoggerFormatter)
    dataLogger.addHandler(dataLoggerHandler)
    dataLogger.setLevel(logging.INFO)

    # HABIP Command Ack logger
    ackLogger = logging.getLogger("acklog")
    ackLoggerHandler = logging.FileHandler(LOG_CMDACK_PATH)
    ackLoggerFormatter = logging.Formatter("%(asctime)s,%(message)s",datefmt="%H:%M:%S")
    ackLoggerHandler.setFormatter(ackLoggerFormatter)
    ackLogger.addHandler(ackLoggerHandler)
    ackLogger.setLevel(logging.INFO)

    # Then use logger.info(stringToAddHere) to add a string to a log file
    
    # Main loop
    while True:
        # Get newly received packets from axreader
        packets = reader.getNewData()

        # Flag if received data
        receivedData = False

        # List of values of HABIP sensors for telemetry data. 64 sensor data points
        habipSensorData = ["NULL"] * 64

        # HABIP Sensors for telemetry data. Values are the index of the list the values are in
        habipSensors = {
            "B0:TB0": 0,
            "B0:TB1": 1,
            "B0:TE0": 2,
            "B0:TE1": 3,
            "B0:TD0": 4,
            "B0:P0": 5,
            "B0:P1": 6,
            "B0:H": 7,
            "B0:V": 8,
            "B0:C": 9,
            "B1:TB0": 10,
            "B1:TB1": 11,
            "B1:TE0": 12,
            "B1:TE1": 13,
            "B1:TD0": 14,
            "B1:P0": 15,
            "B1:P1": 16,
            "B1:H": 17,
            "B1:V": 18,
            "B1:C": 19,
            "B2:TB0": 20,
            "B2:TB1": 21,
            "B2:TE0": 22,
            "B2:TE1": 23,
            "B2:TD0": 24,
            "B2:P0": 25,
            "B2:P1": 26,
            "B2:H": 27,
            "B2:V": 28,
            "B2:C": 29,
            "B3:TB0": 30,
            "B3:TB1": 31,
            "B3:TE0": 32,
            "B3:TE1": 33,
            "B3:TD0": 34,
            "B3:P0": 35,
            "B3:P1": 36,
            "B3:H": 37,
            "B3:V": 38,
            "B3:C": 39,
            "B4:TB0": 40,
            "B4:P0": 41,
            "B4:PB": 42,
            "B4:V": 43,
            "B4:C": 44,
            "B4:XGY": 45,
            "B4:XAC": 46,
            "B4:YGY": 47,
            "B4:YAC": 48,
            "B4:ZGY": 49,
            "B4:ZAC": 50,
            "B4:MS": 51,
            "B4:MC": 52,
            "B4:MV": 53,
            "B4:MD": 54,
            "B4:ME": 55,
            "B5:TB0": 56,
            "B5:TD0": 57,
            "B5:P0": 58,
            "B5:LAT": 59,
            "B5:LON": 60,
            "B5:TM": 61,
            "B5:SPD": 62,
            "B5:ALT": 63,
            "B5:TBL": 64,
            "B5:PBL": 65,
        }

        # Loop through newly received packets
        for packet in packets:
            # Get the data/command portion (relevant portion) of the received packet
            packetDataString = packet.data
            #print packet.data
            #print "--------"

            # If received command acknowledgement(s)
            if "ACK" in packetDataString:
                # Split the acknowledgements if received multiple
                ackList = packetDataString.split(";")

                # Add the acknowledgements to the command acknowledgement log file
                for ack in ackList:
                    ackLogger.info(ack)

            # Else received telemetry data
            else:
                # Received data in the latest packets
                receivedData = True

                # Split the data from the various censors (semicolon separated)
                dataList = packetDataString.split(";")

                # Loop through the sensor data received
                for data in dataList:
                    # Data goes boardNum:sensorAbbrev:value
                    dataParts = data.split(":")

                    # Grab the boardNum:sensorAbbrev portion of the data
                    sensor = dataParts[0] + ":" + dataParts[1]

                    # Grab the value for the sensor
                    value = dataParts[2]

                    # Add the value to the sensor data list if it is a valid sensor
                    if sensor in habipSensors.keys():
                        habipSensorIndex = habipSensors[sensor]
                        habipSensorData[habipSensorIndex] = value

        # Log data for all sensors if received any
        if receivedData:
            # Loop through the sensor data list and add the sensor values to the data log file, comma-separated
            dataToStoreString = ""
            for sensorData in habipSensorData:
                dataToStoreString += sensorData + ","
            dataLogger.info(dataToStoreString)

        # Sleep a bit
        common.msleep(1000)
