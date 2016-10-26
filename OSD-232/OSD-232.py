#!/usr/bin/env python

"""
file: OSD-232.py
author: Connor Goldberg
project: High Altitude Balloon Instrumentation Platform
description: Abstracts the serial interface for the OSD-232 analog video
    overlay board
"""

import serial
import time

msleep = lambda t: time.sleep(t/1000.0)

def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

class OSD232(object):

    command = enum( mode = chr(128),
                    position = chr(129),
                    clearScreen = chr(130),
                    visable = chr(131),
                    translucent = chr(132),
                    backgroundColor = chr(133),
                    zoom = chr(134),
                    zoom = chr(135),
                    characterColor = chr(136),
                    characterBlink = chr(137),
                    reset = chr(138),
                    setVerticalOffset = chr(139),
                    setHorizontalOffset = chr(140)
                    )
    
    screenMode = enum(  overlay = chr(0),
                        fullScreen = chr(1)
                        )
    
    backgroundColor = enum( black = chr(0),
                            blue = chr(1),
                            green = chr(2),
                            cyan = chr(3),
                            red = chr(4),
                            magenta = chr(5),
                            yellow = chr(6),
                            white = chr(7)
                            )

    def __init__(self, port, baudrate=4800):

        # The port is not added within the constructor so the port is not
        # opened automatically
        self.connection = serial.Serial(baudrate=self.baudrate)
        self.connection.port = self.port

    def open(self):
        try:
            self.connection.open()
            print("DEBUG:", "Successfully opened serial connection")
            return True
        except serial.SerialException as e:
            print("ERROR:", e)
            return False

    def close(self):
        self.connection.close()
        print("DEBUG:", "Successfully closed serial connection")

    def sendRaw(self, *data):
        """
        inputs:
            data - characters or strings that get merged and sent over the
                    serial connection
        outputs:
            bool - returns True if the data was written; False otherwise
        """
        byteString = "".join([s for s in data])
        bytesWritten = self.connection.write(byteString)
        if byteString and bytesWritten:
            print("DEBUG:", "Successfully wrote serial data: {}".format(byteString))
            return True
        else:
            print("ERROR:", "Did not write serial data: {}".format(byteString))
            return False

    def setPosition(self, x, y):
        """
        inputs:
            x: Int - the x position of the cursor between 1 and 28
            y:Int - the y position of the cursor between 1 and 11
        outputs:
            bool - returns True if the data was sent; False if otherwise
        """
        x = x if x > 0 and x < 29 else 1
        y = y if y > 0 and y < 12 else 1
        
        print("DEBUG:", "Moving cursor position to {}, {}".format(x, y))
        return self.sendRaw(self.command.position, chr(x), chr(y))

    def setScreenMode(self, mode):
        if mode == self.screenMode.overlay or mode == self.screenMode.fullScreen:
            return self.sendRaw(self.command.mode, mode)
        else:
            return False
