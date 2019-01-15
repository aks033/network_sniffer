from scapy.all import IP
from scapy.all import sniff
from scapy.layers import http
import dpkt
import threading
import time
import operator
from datetime import datetime
from datetime import timedelta
import config
from termcolor import colored
import logging
from collections import Counter
import sniffer

def display_most_hits(url_dict, url_path_counter):
	while(True):
		#print url_path_counter
		if len(url_path_counter) > 0:
			#sorted_traffic = sorted(url_dict.items(), key=operator.itemgetter(1), reverse=True)[:10]
			sorted_traffic = sorted(url_path_counter.items(), key=url_path_counter.get, reverse=True)[0:3]
			print "\n\n-------------------------------------------------Network Traffic -------------------------------------------------"
			print "------------------------------------------------------------------------------------------------------------------"
			print "                                                  Most URL Hits                                                   "
			print "------------------------------------------------------------------------------------------------------------------"
			print "------------------------------------------------------------------------------------------------------------------"
			for key,value in sorted_traffic:
				print "{:64s}:{:50d}".format(key,value)
			print "------------------------------------------------------------------------------------------------------------------\n"
		time.sleep(10)


def examine_traffic_behaviour(traffic_queue, high_traffic_flag):
	global total_url_hits_per_min
	while(True):

		if(len(traffic_queue > 500)):
			traffic_queue = traffic_queue[tr]

		if((datetime.now() - traffic_queue[-1:][0][1]).total_seconds() > 30):
					
			traffic_queue.append((total_url_hits_per_min, datetime.now()))
			
			print traffic_queue
			#print "in examine thread", total_url_hits_per_min
			traffic_last_two_mins = sum(x[0] for x in traffic_queue[-4:])

			if(traffic_last_two_mins > avg_hits):
				generate_high_traffic_alert(traffic_last_two_mins, traffic_queue[-1:][0][1])
				high_traffic_flag = True
			
			elif (high_traffic_flag and traffic_last_two_mins < avg):
				high_traffic_flag = False
				generate_recovered_high_traffic_alert()

			total_url_hits_per_min = 0

def generate_high_traffic_alert(url_hits, time_of_alert):

	print colored("HIGH TRAFFIC GENERATED AN ALERT","red")
	print colored("URL HITS : {}".format(url_hits),"red")
	print colored("TRIGGERED AT : {}".format(time_of_alert),"red")


def generate_recovered_high_traffic_alert():
	print colored("RECOVERED FROM HIGH TRAFFIC", "green")


def main():
	# dictionary to keep a count of urls
	url_dict = {}
	total_url_hits_in_two_mins = 0
	avg_hits = config.initial_anticipated_avg
	traffic_queue = [(0,datetime.now())]
	total_url_hits_per_min = 0
	high_traffic_flag = False
	url_counter = Counter()
	packet_sniffer = sniffer.Sniffer(config.dev, url_counter)
	logging.basicConfig(filename = config.log_file, level=logging.INFO)

	t1 = threading.Thread(target=display_most_hits, args=(url_dict, url_counter))
	t1.start()
	t2 = threading.Thread(target=examine_traffic_behaviour, args=(traffic_queue, high_traffic_flag))
	#t2.start()
	packet_sniffer.start()
	


if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt():
		os_.exit(0)