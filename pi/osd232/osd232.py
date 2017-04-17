"""
file: OSD232.py
author: Connor Goldberg
project: High Altitude Balloon Instrumentation Platform
description: Abstracts the serial interface for the OSD-232 analog video
    overlay board
"""
import serial

import common
import logger
import uart

class osd232(object):

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
    commandName = {v: k for k, v in command.iteritems()}
    
    # Screen mode to char lookup
    screenMode = { 
                    "overlay" : chr(0),
                    "fullScreen" : chr(1)
                    }
    screenModeName = {v: k for k, v in screenMode.iteritems()}

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
        # self.connection = serial.Serial(baudrate=baudrate)
        self.connection = uart.uart(port, baudrate)

        # Create the logger
        self.logger = logger.logger("osd232")
        
        if not self.connection.open():
        	self.logger.log.error("Could not open uart interface")
        else:
        	self.logger.log.info("Opened uart interface for osd")


    def clearScreen(self):
        self.logger.log.info("Clearing screen")
        self.connection.sendRaw(self.command["clearScreen"])

        # Sleep for 10 milliseconds as per the documentation
        # It seems sometimes it takes longer to reset the board, 1 sec is safe
        common.msleep(1000)


    def resetSettings(self):
        self.logger.log.info("Resetting settings")
        self.connection.sendRaw(self.command["reset"])

        # Sleep for 10 milliseconds as per the documentation
        # It seems sometimes it takes longer to reset the board, 1 sec is safe
        common.msleep(1000)


    def display(self, data):
        self.logger.log.info("Displaying on osd: {}".format(data))
        self.connection.sendRaw(data)

    def setBackgroundColor(self, backgroundColor):
        """
        inputs:
            mode: self.color - the background color while in full screen mode
        outputs:
            bool - returns True if the data was sent; False if otherwise
        """
        if backgroundColor in self.color.values():
            self.logger.log.info("Setting screen color to: {}". \
                format(self.color_name[backgroundColor]))
            return self.connection.sendRaw(self.command["backgroundColor"], \
                backgroundColor)
        else:
            self.logger.log.error("Color invalid: {}".format(str(backgroundColor)))
            return False


    def setCharacterBlink(self, characterShouldBlink):
        """
        inputs:
            characterShouldBlink: bool - whether the characters should blink
        outputs:
            bool - returns True if the data was sent; False if otherwise
        """
        if type(characterShouldBlink) is bool:
            self.logger.log.info("Setting character blink to: {}". \
                format(str(characterShouldBlink)))
            return self.connection.sendRaw(self.command["characterBlink"], \
                chr(characterShouldBlink))
        else:
            self.logger.log.error("characterShouldBlink is not bool: {}". \
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
            self.logger.log.info("Setting character color to: {}". \
                format(self.color_name[characterColor]))
            return self.connection.sendRaw(self.command["characterColor"], \
                characterColor)
        else:
            self.logger.log.error("Color invalid: {}".format(str(characterColor)))
            return False


    def setHorizontalOffset(self, horizontalOffset):
        """
        inputs:
            horizontalOffset: Int - text screen position offset (1-63)
        outputs:
            bool - returns True if the data was sent; False if otherwise
        """
        if horizontalOffset < 1 or horizontalOffset > 63:
            self.logger.log.error("Offset must be between 1 and 63, not: {}". \
                format(row))
            return False
        else:
            self.logger.log.info("Setting horizontal offset to: {}". \
                format(horizontalOffset))
            return self.connection.sendRaw(self.command["setHorizontalOffset"], \
                chr(horizontalOffset))


    def setScreenMode(self, screenMode):
        """
        inputs:
            mode: self.screenMode - the mode for the screen to be in
        outputs:
            bool - returns True if the data was sent; False if otherwise
        """
        if screenMode in self.screenMode.values():
            self.logger.log.info("Setting screen mode to: {}". \
                format(self.screenModeName[screenMode]))
            return self.connection.sendRaw(self.command["screenMode"], screenMode)
        else:
            self.logger.log.error("Screenmode invalid: {}". \
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
        
        self.logger.log.info("Moving cursor position to {}, {}".format(row, column))
        return self.connection.sendRaw(self.command["position"], chr(column), chr(row))


    def showText(self, shouldShowText):
        """
        inputs:
            shouldShowText: bool - whether to display the text or not
        outputs:
            bool - returns True if the data was sent; False if otherwise
        """
        if type(shouldShowText) is bool:
            self.logger.log.info("Setting show text to: {}".format(str(shouldShowText)))
            return self.connection.sendRaw(self.command["visable"], chr(shouldShowText))
        else:
            self.logger.log.error("shouldShowText is not bool: {}". \
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
            self.logger.log.info("Setting translucent text to: {}". \
                format(str(shouldBeTranslucent)))
            return self.connection.sendRaw(self.command["translucent"], \
                chr(shouldBeTranslucent))
        else:
            self.logger.log.error("shouldBeTranslucent is not bool: {}". \
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
            self.logger.log.error("Offset must be between 1 and 63, not: {}". \
                format(row))
            return False
        else:
            self.logger.log.info("Setting vertical offset to: {}". \
                format(verticalOffset))
            return self.connection.sendRaw(self.command["setVerticalOffset"], \
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
            self.logger.log.error("Row must be between 1 and 11, not: {}". \
                format(row))
            return False
        elif horizontalZoom < 1 or horizontalZoom > 4:
            self.logger.log.error("Horizontal zoom must be between 1 and 4, not: {}". \
                format(row))
            return False
        elif verticalZoom < 1 or verticalZoom > 4:
            self.logger.log.error("Vertical zoom must be between 1 and 4, not: {}". \
                format(row))
            return False
        else:
            self.logger.log.info("Setting row {} zoom to be {}, {}". \
                format(row, horizontalZoom, verticalZoom))
            return self.connection.sendRaw(self.command["zoom"], row, horizontalZoom, \
                verticalZoom)
