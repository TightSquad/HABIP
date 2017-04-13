"""
author: Connor Goldberg
project: High Altitude Balloon Instrumentation Platform
description: Reads the axlisten log file
"""

import logger

class ax25packet(object):

	def __init__(self):
		self.interface = ""
		self.source = ""
		self.destination = ""
		self.length = ""
		self.data = ""

	def __str__(self):
		return "interface: {}\nsource: {}\ndestination: {}\nlength: {}\ndata: {}".format(self.interface, self.source, self.destination, self.length, self.data)

	def isComplete(self):
		return True if (self.interface and self.source and self.destination and self.length and self.data) else False

	@staticmethod
	def parseFromList(lst):
		packet = ax25packet()
		header = lst[0].split(' ')
		dataLines = lst[1:]

		getfm = False
		getto = False
		getlen = False
		for item in header:
			if not packet.interface and item.endswith(':'):
				packet.interface = item.strip(':')
				continue

			if item == "fm":
				getfm = True
				continue

			if getfm:
				packet.source = item
				getfm = False
				continue

			if item == "to":
				getto = True
				continue

			if getto:
				packet.destination = item
				getto = False
				continue

			if item == "len":
				getlen = True
				continue

			if getlen:
				packet.length = item
				getlen = False
				continue

		dataString = ""
		for item in dataLines:
			parts = item.split("  ")
			if len(parts) < 2:
				print "ERROR: could not decode data line: {}".format(item)
				dataString = ""
				break
			else:
				dataString += parts[1].strip()

		packet.data = dataString
		return packet


class axreader(object):

	def __init__(self, filePath, interfaces=None, sources=None, destinations=None):
		"""
		filePath - path to the output log file from axlisten
		source - a list of source callsigns to whitelist
		destinations - a list of destination call signs to whitelist
		"""

		self.logger = logger.logger("axreader")

		self.filePath = filePath

		if type(interfaces) in [type(None), list]:
			self.interfaces = interfaces
		elif type(interfaces) is str:
			self.interfaces = [interfaces]
		else:
			self.logger.log.error("Invalid type for interfaces: {}".format(type(interfaces)))
			self.interfaces = None

		if type(sources) in [type(None), list]:
			self.sources = sources
		elif type(sources) is str:
			self.sources = [sources]
		else:
			self.logger.log.error("Invalid type for sources: {}".format(type(sources)))
			self.sources = None

		if type(destinations) in [type(None), list]:
			self.destinations = destinations
		elif type(destinations) is str:
			self.destinations = [destinations]
		else:
			self.logger.log.error("Invalid type for destinations: {}".format(type(destinations)))
			self.destinations = None

		self.logger.log.debug("Created axlogger instance with sources whitelist: {} and destinations whitelist: {}".format(sources, destinations))

		self.fileHandle = None
		self.isOpen = False

		self.open()

	def open(self):
		try:
			self.fileHandle = open(self.filePath)
		except Exception as e:
			self.logger.log.error("Could not open file: {}, exception: {}".format(self.filePath, e))
			return False

		self.logger.log.debug("Opened {}".format(self.filePath))		
		self.fileHandle.seek(0,2) # Seek to the end of the log file
		self.isOpen = True
		return True

	def getNewLines(self):
		lines = []
		line = self.fileHandle.readline()
		while line:
			lines.append(line)
			line = self.fileHandle.readline()

		lines = [line.strip() for line in lines]
		return lines

	def getNewData(self):
		packets = []

		lines = self.getNewLines()
		rawPackets = self.separatePackets(lines)

		if not rawPackets:
			return None
		else:
			for rawPacket in rawPackets:
				packet = ax25packet.parseFromList(rawPacket)

				# Filter out packets we don't care about
				if not packet.isComplete():
					continue

				if self.interfaces and packet.interface not in self.interfaces:
					continue

				if self.sources and packet.source not in self.sources:
					continue

				if self.destinations and packet.destination not in self.destinations:
					continue

				packets.append(packet)

		return packets

	def separatePackets(self, lines):
		packetLines = []
		buf = []
		for line in lines:
			if "fm" in line and "to" in line and "len" in line:
				# Got a header
				if buf:
					packetLines.append(buf)
					buf = [line]
					continue
			buf.append(line)
		
		if buf:
			packetLines.append(buf)

		return packetLines
