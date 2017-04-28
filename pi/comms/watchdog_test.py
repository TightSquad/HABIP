#!/usr/bin/env python

# Pet the dog son

import common
import gpio
import watchdog

def main():
	g = gpio.gpio()
	w = watchdog.watchdog(gpio=g)

	while True:
		w.pet()
		common.msleep(10*1000)

if __name__ == '__main__':
	main()
