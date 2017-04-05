#!/usr/bin/env python

# uart test

import uart

PORT = "/dev/ttyAMA0"
# PORT = "/dev/tty.usbserial"
# PORT = "/dev/tty.usbserial-A402ZBV2"

BAUDRATE = 115200

def send(con):
	con.sendRaw("Testing!!"+uart.EOT)

def recv(con):
	data = con.readUntil(uart.EOT)
	print data

def main():
	con = uart.uart(port=PORT, baudrate=BAUDRATE)
	con.open()
	# send(con)
	recv(con)
	con.close()

if __name__ == "__main__":
	main()
