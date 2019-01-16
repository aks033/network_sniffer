from threading import Thread
import time
import operator
from datetime import datetime, timedelta
from termcolor import colored

class Alert(Thread):

	def __init__(self, sniffer_obj, avg):
		super(Alert, self).__init__()
		#self.traffic_queue = traffic_queue
		self.high_traffic_flag = False
		self.avg_hits = avg
		self.sniffer_obj = sniffer_obj

	def run(self):
		self.examine_traffic_behaviour()

	def examine_traffic_behaviour(self):
		#global total_url_hits_per_min
		while(True):

			#if((datetime.now() - traffic_queue[-1:][0][1]).total_seconds() > 30):
						
			#traffic_queue.append((total_url_hits_per_min, datetime.now()))

			#print self.traffic_queue
			#print "in examine thread", total_url_hits_per_min
			#traffic_last_two_mins = sum(x[0] for x in traffic_queue[-4:])
			time_of_last_hit = self.sniffer_obj.traffic_queue[-1:]
			start_time_of_traffic_eval = datetime.now() - timedelta(seconds=120)
			self.sniffer_obj.traffic_queue = [i for i in self.sniffer_obj.traffic_queue if i[0] >= start_time_of_traffic_eval]
			traffic_last_two_mins = len(self.sniffer_obj.traffic_queue)
			print(self.sniffer_obj.traffic_queue)
			if(traffic_last_two_mins > self.avg_hits):
				self.generate_high_traffic_alert(traffic_last_two_mins, time_of_last_hit[0])
				self.high_traffic_flag = True

			elif (self.high_traffic_flag and traffic_last_two_mins < self.avg_hits):
				self.high_traffic_flag = False
				self.generate_recovered_high_traffic_alert(time_of_last_hit[0])

			time.sleep(20)

	def generate_high_traffic_alert(self, url_hits, time_of_alert):

		print colored("HIGH TRAFFIC GENERATED AN ALERT","red")
		print colored("URL HITS : {}".format(url_hits),"red")
		print colored("TRIGGERED AT : {}".format(time_of_alert[0]),"red")


	def generate_recovered_high_traffic_alert(self, recovery_time):
		print colored("RECOVERED FROM HIGH TRAFFIC AT {}".format(recovery_time[0]), "green")