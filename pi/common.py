"""
author: Connor Goldberg
project: High Altitude Balloon Instrumentation Platform
description: Common functions and values
"""

import time

msleep = lambda t: time.sleep(t/1000.0)
usleep = lambda t: time.sleep(t/1000000.0)

def flatten(lst):
	"""
	Accepts a list/tuple of lists/tuples of lists/tuples of ... and flattens it
	example:
		>>> flatten([1,(2,[3,4]),5])
		[1,2,3,4,5]
	"""
	
	l = []
	for item in lst:
		if type(item) is list or type(item) is tuple:
			l += flatten(item)
		else:
			l.append(item)
	return l

def reverseBits(byte):
	"""
	Reverses the bits in an 8-bit byte
	"""
	byte = ((byte & 0xF0) >> 4) | ((byte & 0x0F) << 4)
	byte = ((byte & 0xCC) >> 2) | ((byte & 0x33) << 2)
	byte = ((byte & 0xAA) >> 1) | ((byte & 0x55) << 1)
	return byte
