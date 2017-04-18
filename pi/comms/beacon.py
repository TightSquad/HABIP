"""
author: Connor Goldberg
project: High Altitude Balloon Instrumentation Platform
description: Soundmodem beacon functionality
"""

import subprocess
import logger

class beacon(object):
	"""
	Send data over the soundmodem beacon interface
	"""

	def __init__(self, interface, source, destination):

		self.logger = logger.logger("beacon")

		self.interface = interface
		self.source = source
		self.destination = destination

	def send(self, data):
		cmd = ["beacon", "-c", self.source, "-d", self.destination, "-s", self.interface, data]
		try:
			subprocess.Popen(cmd)
			self.logger.log.debug("Called: $ {}".format(" ".join(cmd)))
		except Exception as e:
			self.logger.log.error("Got exception in beacon: {}".format(e))


##### Testing

if __name__ == '__main__':
	b = beacon("sm0", "W2RIT-11", "W2RIT")
	print b.send("Testing")
