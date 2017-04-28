#!/usr/bin/env python

# Testing the daqcs comms

import common
import interfaces


def main():

	intf = interfaces.interfaces()
	intf.openspi()
	intf.opendaqcs()

	d = intf.daqcs


	while True:
		print "----------"
		print d.currentState

		# d.queueCommand("{06:1491592543}")
		# d.queueCommand("{05:B0}")
		# d.queueCommand("{06:1491592543}")
		d.update()

		for name, board in intf.boards.iteritems():
			print "Data for board: {}".format(name)
			board.printAllData()

		common.msleep(3000)


if __name__ == '__main__':
	main()