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

		self.interface = interface
		self.url_counter = counter
		self.traffic_queue = traffic_queue
		self.packet_list = []
		self.ip_list = Counter()


	def run(self):
		sniff(iface = self.interface, filter='tcp', prn=self.sniff_urls)

	def sniff_urls(self, packet):		

		if packet.haslayer(http.HTTPRequest):
			http_layer = packet.getlayer(http.HTTPRequest)
			ip_layer = packet.getlayer(IP)
			logging.info('\n{0[src]} - {1[Method]}- http://{1[Host]}{1[Path]}'.format(ip_layer.fields, http_layer.fields))
			self.ip_list.update([ip_layer.fields["dst"]])
			#print packet.show()
			#print http_layer.fields
			
			url_key = http_layer.fields["Host"]

			#print http_layer.fields["Path"], http_layer.fields["Path"].strip('/').split('/')

			path = http_layer.fields["Path"].strip('/').split('/')

			if(len(path) > 0 and path[0] != ""):
				url_key = url_key + "/"+ path[0]
				self.url_counter.update([url_key])
				self.traffic_queue.append((datetime.now(), url_key))
				#print "sniffer ::",self.traffic_queue
			