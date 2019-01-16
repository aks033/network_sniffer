#from scapy.all import IP
#from scapy.all import sniff
#from scapy.layers import http
#import dpkt
import threading
import time
#import operator
from datetime import datetime
from datetime import timedelta
import config
#from termcolor import colored
import logging
from collections import Counter
import sniffer
import display
import alert


def main():
	# dictionary to keep a count of urls
	#url_dict = {}
	#total_url_hits_in_two_mins = 0
	avg_hits = config.initial_anticipated_avg
	traffic_queue = []
	#total_url_hits_per_min = 0
	#high_traffic_flag = False
	url_counter = Counter()
	packet_sniffer = sniffer.Sniffer(config.dev, url_counter, traffic_queue)
	alerts = alert.Alert(packet_sniffer, avg_hits)
	most_hits_display = display.Display(url_counter)
	logging.basicConfig(filename = config.log_file, level=logging.INFO)

	#t1 = threading.Thread(target=display_most_hits, args=(url_dict, url_counter))
	#t1.start()
	#t2 = threading.Thread(target=examine_traffic_behaviour, args=(traffic_queue, high_traffic_flag))
	#t2.start()
	packet_sniffer.start()
	#most_hits_display.start()
	alerts.start()
	#threading.Timer(30, alerts.examine_traffic_behaviour).start()

	

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt():
		os_.exit(0)