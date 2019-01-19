import threading
import config
import logging
from collections import Counter
import sniffer
import display
import alert
import signal
import os
import sys


def main():
	''' main function to run the application'''

	avg_hits = config.initial_anticipated_avg #static value of avg hits
	traffic_queue = [] # keeps a tuple of (time of packet, url)
	url_counter = Counter() # keeps a count of url section

	# instances of classes - packet sniffer, alert and display 
	packet_sniffer = sniffer.Sniffer(config.dev, url_counter, traffic_queue)
	alerts = alert.Alert(packet_sniffer, avg_hits)
	app_display = display.Display(packet_sniffer, alerts)

	try:
		#log configuration 
		path = os.path.dirname(os.getcwd())
		logging.basicConfig(filename = path+config.log_file, level=logging.INFO)
	except IOError as e :
		print str(e)

	try:
		#start all threads
		packet_sniffer.start()
		app_display.start()
		alerts.start()

		signal.pause()
	
	except KeyboardInterrupt:
		os._exit(1)

if __name__ == '__main__':
	main()