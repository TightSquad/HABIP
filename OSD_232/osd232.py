#!/usr/bin/env python

"""
file: OSD232.py
author: Connor Goldberg
project: High Altitude Balloon Instrumentation Platform
description: Abstracts the serial interface for the OSD-232 analog video
    overlay board
"""

import serial
import time

msleep = lambda t: time.sleep(t/1000.0)

class OSD232(object):

    # Command to char lookup
    command = {
                "mode" : chr(128),
                "position" : chr(129),
                "clearScreen" : chr(130),
                "visable" : chr(131),
                "translucent" : chr(132),
                "backgroundColor" : chr(133),
                "zoom" : chr(134),
                "characterColor" : chr(135),
                "characterBlink" : chr(136),
                "reset" : chr(137),
                "setVerticalOffset" : chr(138),
                "setHorizontalOffset" : chr(139)
                }
    command_name = {v: k for k, v in command.iteritems()}
    
    # Screen mode to char lookup
    screenMode = { 
                    "overlay" : chr(0),
                    "fullScreen" : chr(1)
                    }
    screenMode_name = {v: k for k, v in screenMode.iteritems()}

    # Color to char lookup
    color = { 
                "black" : chr(0),
                "blue" : chr(1),
                "green" : chr(2),
                "cyan" : chr(3),
                "red" : chr(4),
                "magenta" : chr(5),
                "yellow" : chr(6),
                "white" : chr(7)
                }
    color_name = {v: k for k, v in color.iteritems()}
    
    # Special symbol character lookup
    symbol = {
                "square" : chr(0+0),
                "clock" : chr(15+0),
                "bar0" : chr(10+16),
                "bar1" : chr(11+16),
                "bar2" : chr(12+16),
                "bar3" : chr(13+16),
                "bar4" : chr(14+16),
                "bar5" : chr(15+16),
                "triangle" : chr(12+32),
                "cleff" : chr(11+48),
                "heart" : chr(12+48),
                "key" : chr(14+48),
                "satellite" : chr(0+64),
                "rightArrow" : chr(11+80),
                "leftArrow" : chr(12+80),
                "upArrow" : chr(13+80),
                "downArrow" : chr(14+80),
                "pipe0" : chr(11+112),
                "pipe1" : chr(12+112),
                "pipe2" : chr(13+112),
                "pipe3" : chr(14+112),
                "pipe4" : chr(15+112)
                }

    # Class members
    def __init__(self, port, baudrate=4800):
        """
        inputs:
            port: String - The serial port of where to access the OSD board
            baudrate: Int - The configured baudrate of the OSD (if the jumper
                            on the device is on, the baudrate is 4800. If the
                            jumper is removed, the baudrate is 2400)
        outputs:
            returns a reference to the instantiated class
        """

        # The port is not added as a parameter to the constructor so the port
        # is not opened automatically
        self.connection = serial.Serial(baudrate=baudrate)
        self.connection.port = port

    def open(self):
        """
        inputs:
            none
        outputs:
            bool - returns True if the port is opened, else False
        """
        try:
            self.connection.open()
            print("INFO:", "Successfully opened serial connection port: {}". \
                format(self.connection.port))
            return True
        except serial.SerialException as e:
            print("ERROR:", e)
            return False

    def close(self):
        msleep(1000) # Wait for a second to make sure all the data is out
        self.connection.close()
        print("INFO:", "Successfully closed serial port: {}". \
            format(self.connection.port))

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
        self.connection.flush() # Wait for the output to be written
        if byteString and bytesWritten:
            print("DEBUG:", \
                "Successfully wrote serial data: {}".format(byteString))
            return True
        else:
            print("ERROR:", "Did not write serial data: {}".format(byteString))
            return False

    #################### Helper functions ####################

    def clearScreen(self):
        print("INFO: Clearing screen")
        self.sendRaw(self.command["clearScreen"])

        # Sleep for 10 milliseconds as per the documentation
        msleep(10)

    def resetSettings(self):
        print("INFO: Resetting settings")
        self.sendRaw(self.command["reset"])

        # Sleep for 10 milliseconds as per the documentation
        # It seems sometimes it takes longer to reset the board, 1 sec is safe
        msleep(1000)

    def setBackgroundColor(self, backgroundColor):
        """
        inputs:
            mode: self.color - the background color while in full screen mode
        outputs:
            bool - returns True if the data was sent; False if otherwise
        """
        if backgroundColor in self.color.values():
            print("INFO: Setting screen color to: {}". \
                format(self.color_name[backgroundColor]))
            return self.sendRaw(self.command["backgroundColor"], \
                backgroundColor)
        else:
            print("ERROR: Color invalid: {}".format(str(backgroundColor)))
            return False

    def setCharacterBlink(self, characterShouldBlink):
        """
        inputs:
            characterShouldBlink: bool - whether the characters should blink
        outputs:
            bool - returns True if the data was sent; False if otherwise
        """
        if type(characterShouldBlink) is bool:
            print("INFO: Setting character blink to: {}". \
                format(str(characterShouldBlink)))
            return self.sendRaw(self.command["characterBlink"], \
                chr(characterShouldBlink))
        else:
            print("ERROR: characterShouldBlink is not bool: {}". \
                format(str(characterShouldBlink)))
            return False

    def setCharacterColor(self, characterColor):
        """
        inputs:
            characterColor: self.color - specify the color to write next
        outputs:
            bool - returns True if the data was sent; False if otherwise
        """
        if characterColor in self.color.values():
            print("INFO: Setting character color to: {}". \
                format(self.color_name[characterColor]))
            return self.sendRaw(self.command["characterColor"], \
                characterColor)
        else:
            print("ERROR: Color invalid: {}".format(str(characterColor)))
            return False

    def setHorizontalOffset(self, horizontalOffset):
        """
        inputs:
            horizontalOffset: Int - text screen position offset (1-63)
        outputs:
            bool - returns True if the data was sent; False if otherwise
        """
        if horizontalOffset < 1 or horizontalOffset > 63:
            print("ERROR: Offset must be between 1 and 63, not: {}". \
                format(row))
            return False
        else:
            print("INFO: Setting horizontal offset to: {}". \
                format(horizontalOffset))
            return self.sendRaw(self.command["setHorizontalOffset"], \
                chr(horizontalOffset))

    def setScreenMode(self, screenMode):
        """
        inputs:
            mode: self.screenMode - the mode for the screen to be in
        outputs:
            bool - returns True if the data was sent; False if otherwise
        """
        if screenMode in self.screenMode.values():
            print("INFO: Setting screen mode to: {}". \
                format(self.screenMode_name[screenMode]))
            return self.sendRaw(self.command["screenMode"], screenMode)
        else:
            print("ERROR: Screenmode invalid: {}". \
                format(str(screenMode)))
            return False

    def setPosition(self, row=1, column=1):
        """
        inputs:
            x: Int - the x position of the cursor between 1 and 28
            column: Int - the column position of the cursor between 1 and 11
        outputs:
            bool - returns True if the data was sent; False if otherwise
        """
        row = row if row > 0 and row < 29 else 1
        column = column if column > 0 and column < 12 else 1
        
        print("INFO:", "Moving cursor position to {}, {}".format(row, column))
        return self.sendRaw(self.command["position"], chr(column), chr(row))

    def showText(self, shouldShowText):
        """
        inputs:
            shouldShowText: bool - whether to display the text or not
        outputs:
            bool - returns True if the data was sent; False if otherwise
        """
        if type(shouldShowText) is bool:
            print("INFO: Setting show text to: {}".format(str(shouldShowText)))
            return self.sendRaw(self.command["visable"], chr(shouldShowText))
        else:
            print("ERROR: shouldShowText is not bool: {}". \
                format(str(shouldShowText)))
            return False

    def setTranslucentText(self, shouldBeTranslucent):
        """
        inputs:
            shouldBeTranslucent: bool - whether to translucent the text or not
        outputs:
            bool - returns True if the data was sent; False if otherwise
        """
        if type(shouldBeTranslucent) is bool:
            print("INFO: Setting translucent text to: {}". \
                format(str(shouldBeTranslucent)))
            return self.sendRaw(self.command["translucent"], \
                chr(shouldBeTranslucent))
        else:
            print("ERROR: shouldBeTranslucent is not bool: {}". \
                format(str(shouldBeTranslucent)))
            return False

    def setVerticalOffset(self, verticalOffset):
        """
        inputs:
            verticalOffset: Int - text screen position offset (1-63)
        outputs:
            bool - returns True if the data was sent; False if otherwise
        """
        if verticalOffset < 1 or verticalOffset > 63:
            print("ERROR: Offset must be between 1 and 63, not: {}". \
                format(row))
            return False
        else:
            print("INFO: Setting vertical offset to: {}". \
                format(verticalOffset))
            return self.sendRaw(self.command["setVerticalOffset"], \
                chr(verticalOffset))

    def setZoom(self, row=1, horizontalZoom=1, verticalZoom=1):
        """
        inputs:
            row: Int - specify what row to zoom (1-11)
            horizontalZoom: Int - specify the zoom factor (1-4)
            verticalZoom: Int - specify the zoom factor (1-4)
        outputs:
            bool - returns True if the data was sent; False if otherwise
        """
        if row < 1 or row > 11:
            print("ERROR: Row must be between 1 and 11, not: {}". \
                format(row))
            return False
        elif horizontalZoom < 1 or horizontalZoom > 4:
            print("ERROR: Horizontal zoom must be between 1 and 4, not: {}". \
                format(row))
            return False
        elif verticalZoom < 1 or verticalZoom > 4:
            print("ERROR: Vertical zoom must be between 1 and 4, not: {}". \
                format(row))
            return False
        else:
            print("INFO: Setting row {} zoom to be {}, {}". \
                format(row, horizontalZoom, verticalZoom))
            return self.sendRaw(self.command["zoom"], row, horizontalZoom, \
                verticalZoom)