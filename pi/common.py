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

