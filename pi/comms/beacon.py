"""
author: Connor Goldberg
project: High Altitude Balloon Instrumentation Platform
description: Soundmodem beacon functionality
"""

class beacon(object):
	"""
	Send data over the soundmodem beacon interface
	"""

	def __init__(self, interface, source, destination)