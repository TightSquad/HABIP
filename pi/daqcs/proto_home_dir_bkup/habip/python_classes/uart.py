"""
file: uart.py
author: Connor Goldberg
project: High Altitude Balloon Instrumentation Platform
description: Abstracts some functionality of the uart interface
"""

# sudo apt-get install python-pip
# sudo pip install pyserial
import serial

import common
import logger

class uart(object):
    """
    Abstracts some basic uart functionality from the pyserial module
    """

    SOT = '{' # ASCII Start of Transmission character
    EOT = '}' # ASCII End of Transmission character
    CR = '\r'
    LF = '\n'
    CRLF = CR+LF

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
        except serial.SerialException as e:
            if str(e) != "Port is already open.":
                self.logger.log.error("error in uart.open: {}".format(e))
                return False

        self.logger.log.debug("Successfully opened serial interface port: {}". \
            format(self.interface.port))
        self.isOpen = True
        return True

    def close(self):
        self.interface.close()
        self.isOpen = False
        self.logger.log.debug("Successfully closed serial port: {}". \
            format(self.interface.port))


    def readUntil(self, seq):
        """
        Reads from the uart until it sees the sequence specified by seq
        inputs:
            seq - if seq is a string, it will keep reading until it sees the seq
                    at the end at which point it will return the data without
                    the seq attached
        outputs:
            data - the characters that are read in over the interface
        """
        run = True
        data = ""
        
        if type(seq) is list:
            pass
        elif type(seq) is str:
            seq = [seq]
        else:
            self.logger.log.error("seq parameter is of an invalid type: {}". \
                format(type(seq)))

        while run:
            try:
                data += self.interface.read()
                for item in seq:
                    if data.endswith(item):
                        run = False
            except Exception as e:
                run = False
                self.logger.log.error(e)
                return ""

        self.logger.log.debug("Successfully read serial data: {}". \
            format(data))
        return data

    def sendRaw(self, *data):
        """
        inputs:
            data - characters or strings that get merged and sent over the
                    serial interface
        outputs:
            bool - returns True if the data was written; False otherwise
        """
        byteString = "".join(common.flatten(data))
        try:
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
        except Exception as e:
            self.logger.log.error("Got exception: {}". \
                    format(e))
            self.logger.log.error("Did not write serial data: {}". \
                    format(byteString))
            return False
