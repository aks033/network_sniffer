import unittest 
import time
import sys 
import src.config 
from StringIO import StringIO
import requests
import src.sniffer
import src.display
import src.alert

class AlertTest(unittest.TestCase):

	def setUp(self):

		test_urls = set(["http://www.umass.edu", "http://fossilinsects.myspecies.info", "http://nyu.edu"])

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
		print "setup done"

	def test_alert(self):
		data = sys.stdout
		try:
			print "starting test"
			output = StringIO()
			sys.stdout = output

			#start all threads
			packet_sniffer.start()
			app_display.start()
			alerts.start()

			alerts.start()
			for i in test_urls:	
				request.get(i)

			time.sleep(30)
			response = output.getvalue().strip()
			self.assertTrue("HIGH TRAFFIC" in response)

			time.sleep(180)
			response = output.getvalue().strip()
			self.assertTrue("RECOVERED" in response)

		finally:
			sys.stdout = data


if __name__ == '__main__':
	unittest.main()
