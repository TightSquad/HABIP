#!/usr/bin/env python
import time

import w1
from w1 import read_temp
while True:
	print read_temp(sensor_index=0)
	print read_temp(sensor_index=1)
	time.sleep(1)

