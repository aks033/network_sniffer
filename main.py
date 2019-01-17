import threading
import time
from datetime import datetime
from datetime import timedelta
import config
import logging
from collections import Counter
import sniffer
import display
import alert


def main():
	''' main function to run the application'''

	avg_hits = config.initial_anticipated_avg #static value of avg hits
	traffic_queue = [] # keeps a tuple of (time of packet, url)
	url_counter = Counter() # keeps a count of url section

	# instances of classes - packet sniffer, alert and display 
	packet_sniffer = sniffer.Sniffer(config.dev, url_counter, traffic_queue)
	alerts = alert.Alert(packet_sniffer, avg_hits)
	app_display = display.Display(packet_sniffer, alerts)

	# logger configuration
	logging.basicConfig(filename = config.log_file, level=logging.INFO)

	packet_sniffer.daemon = True
	app_display.deamon = True
	alerts.daemon = True

	#start all threads
	packet_sniffer.start()
	app_display.start()
	alerts.start()


if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt():
		cleanup_stop_thread()
		sys.exit()