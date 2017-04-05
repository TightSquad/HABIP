"""
file: uart.py
author: Connor Goldberg
project: High Altitude Balloon Instrumentation Platform
description: Abstracts some functionality of the uart interface
"""

import serial

import common
import logger

class uart(object):
    """
    Abstracts some basic uart functionality from the pyserial module
    """

    def __init__(self, port, baudrate):
        self.interface = serial.Serial(baudrate=baudrate)
        self.interface.port = port
        self.isOpen = False

        # Create the logger
        self.logger = logger.logger("uart")


    def open(self):
        """
        inputs:
            none
        outputs:
            bool - returns True if the port is opened, else False
        """
        try:
            self.interface.open()
            self.logger.log.debug("Successfully opened serial interface port: {}". \
                format(self.interface.port))
            self.isOpen = True
            return True
        except serial.SerialException as e:
            self.logger.log.error(e)
            return False


    def close(self):
        self.interface.close()
        self.isOpen = False
        self.logger.log.debug("Successfully closed serial port: {}". \
            format(self.interface.port))


    def sendRaw(self, *data):
        """
        inputs:
            data - characters or strings that get merged and sent over the
                    serial interface
        outputs:
            bool - returns True if the data was written; False otherwise
        """
        byteString = "".join(common.flatten(data))
        bytesWritten = self.interface.write(byteString)
        self.interface.flush() # Wait for the output to be written
        if byteString and bytesWritten:
            self.logger.log.debug("Successfully wrote serial data: {}". \
                format(byteString))
            return True
        else:
            self.logger.log.error("Did not write serial data: {}". \
                format(byteString))
            return False
