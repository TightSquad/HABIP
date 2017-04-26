"""
author: Connor Goldberg
project: High Altitude Balloon Instrumentation Platform
description: Schedules tasks to be called every so often
"""

import logger

class task(object):
	"""
	Object to hold a callback and its frequency to be called at
	"""

	def __init__(self, callback, frequency):
		self.callback = callback
		self.frequency = frequency

	def __repr__(self):
		return "task({},{})".format(self.callback.__name__, self.frequency)

	def __str__(self):
		return self.__repr__()


class scheduler(object):
	"""
	Keeps track of tasks to be called
	"""

	def __init__(self):
		self.logger = logger.logger("scheduler")
		self.count = 0
		self.tasks = []

	def schedule(self, callback, frequency):
		"""
		Schedule a task
		"""

		if type(frequency) is not int:
			self.logger.log.warning("frequency: {} is not an int".format(frequency))
		else:
			t = task(callback=callback, frequency=frequency)
			self.logger.log.info("Scheduled: {}".format(t))
			self.tasks.append(t)

	def update(self):
		"""
		Check for tasks to be called and call them
		"""

		for t in self.tasks:
			if self.count % t.frequency == 0:
				try:
					t.callback()
					self.logger.log.debug("Called {} on count {}".format(t, self.count))
				except Exception as e:
					self.logger.log.warning("Could not execute {} on count {}. Exception: {}".format(t, self.count, e))

		self.count += 1
