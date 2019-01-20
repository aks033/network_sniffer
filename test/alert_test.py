import unittest 
import time
import os 
path = os.path.dirname(os.getcwd())
import sys 
sys.path.insert(0, path)
from src import config
import requests
from src import sniffer
from src import display
from src import alert
from collections import Counter
import logging

class AlertTest(unittest.TestCase):

	def setUp(self):

		self.test_urls = set(["http://www.umass.edu/about", "http://fossilinsects.myspecies.info/about", "http://nyu.edu/careers"])

		avg_hits = 20 #static value of avg hits
		traffic_queue = [] # keeps a tuple of (time of packet, url)
		url_counter = Counter() # keeps a count of url section

		# instances of classes - packet sniffer, alert and display 
		self.packet_sniffer = sniffer.Sniffer(config.dev, url_counter, traffic_queue)
		self.alerts = alert.Alert(self.packet_sniffer, avg_hits)
		self.packet_sniffer.daemon = True
		self.alerts.daemon = True

		# logger configuration
		logging.basicConfig(filename = 'traffic_test', level=logging.INFO)

		
		print "setup done"
		

	def test_alert(self):
		data = sys.stdout
		try:
			print "starting test"

			#start all threads
			self.packet_sniffer.start()
			self.alerts.start()

			# send requests
			print "sending requests...."
			for j in xrange(10):
				for i in self.test_urls:	
					requests.get(i)

			time.sleep(15)
			print "high_traffic_flag:",self.alerts.high_traffic_flag
			self.assertTrue(self.alerts.high_traffic_flag)

			time.sleep(130) # 10 seconds extra in case the alert thread is sleeping at the 2 min mark
			print"recovered_flag:",self.alerts.recovered_flag
			self.assertFalse(self.alerts.high_traffic_flag)
			self.assertTrue(self.alerts.recovered_flag)

		except AssertionError as error:
			print str(error)

		finally:
			print "exiting test"

		

if __name__ == '__main__':
	unittest.main()
