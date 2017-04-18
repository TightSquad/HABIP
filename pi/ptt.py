#!/usr/bin/env python

import sys

import gpio

PTT_PIN = 36

def main():
	g = gpio.gpio()
	g.setPinMode(PTT_PIN, gpio.GPIO.OUT)

	pttMode = 0
	if len(sys.argv) > 1:
		pttMode = sys.argv[1]

	if pttMode == "1":
		g.setHigh(PTT_PIN)
	else:
		g.setLow(PTT_PIN)

if __name__ == "__main__":
	main()
