"""
author: Connor Goldberg
project: High Altitude Balloon Instrumentation Platform
description: Soundmodem beacon functionality
"""

import subprocess

class beacon(object):
	"""
	Send data over the soundmodem beacon interface
	"""

	def __init__(self, interface, source, destination):
		self.interface = interface
		self.source = source
		self.destination = destination

	def send(self, data):
		cmd = ["beacon", "-c", self.source, "-d", self.destination, self.interface, data]
		subprocess.Popen(cmd)

##### Testing

if __name__ == '__main__':
	b = beacon("sm0", "W2RIT-11", "W2RIT")
	print b.send("Testing")
