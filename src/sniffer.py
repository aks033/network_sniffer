from scapy.all import IP
from scapy.all import sniff
from scapy.layers import http
import dpkt
from threading import Thread
import time
import operator
from datetime import datetime
from datetime import timedelta
import config
import logging
from collections import Counter

class Sniffer(Thread):

	def __init__(self, interface, counter, traffic_queue):
		super(Sniffer, self).__init__()

		self.interface = interface # interface from where to sniff traffic
		self.url_counter = counter # counter to amintain url counts
		self.traffic_queue = traffic_queue # to maintain traffic to check traffic for the last 2 mins 
		self.ip_list = Counter() # to keep IP addresses

	def run(self):
		''' to sniff tcp packets on the desired interface'''
		sniff(iface = self.interface, filter='tcp', prn=self.sniff_urls)

	def sniff_urls(self, packet):		
		if packet.haslayer(http.HTTPRequest):
			http_layer = packet.getlayer(http.HTTPRequest) # HTTP fields dictionary
			ip_layer = packet.getlayer(IP) # IP fields dictionary
			logging.info('\n{0[src]} - {1[Method]}- http://{1[Host]}{1[Path]}'.format(ip_layer.fields, http_layer.fields))
			self.ip_list.update([ip_layer.fields["dst"]])
			
			url_key = http_layer.fields["Host"]
			path = http_layer.fields["Path"].strip('/').split('/')
			if(len(path) > 0 and path[0] != ""):
				url_key = url_key + "/"+ path[0]
				self.url_counter.update([url_key])
				self.traffic_queue.append((datetime.now(), url_key))
			