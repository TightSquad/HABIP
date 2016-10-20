#!/usr/bin/env python

import serial


class OSD232(object):

	def __init__(self, port, baudrate=4800):
		self.port = port
		self.baudrate = baudrate
		self.connection = serial.Serial(port=self.port, baudrate=self.baudrate)

	def open(self):
		self.connection.open()

	def close(self):
		self.connection.close()