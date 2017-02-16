"""
author: Connor Goldberg
project: High Altitude Balloon Instrumentation Platform
description: Common functions and values
"""

import time

msleep = lambda t: time.sleep(t/1000.0)
usleep = lambda t: time.sleep(t/1000000.0)
