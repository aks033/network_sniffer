from threading import Thread
import time
import operator
from datetime import datetime, timedelta

class Alert(Thread):
	''' Alert mechanism for the application '''

	def __init__(self, sniffer_obj, avg):
		super(Alert, self).__init__()

		self.high_traffic_flag = False
		self.recovered_flag = False
		self.avg_hits = avg
		self.sniffer_obj = sniffer_obj
		self.alert_time = None
		self.traffic_at_alert_time = None
		self.alert_recovery_time = None

	def run(self):
		self.examine_traffic_behaviour()

	def examine_traffic_behaviour(self):

		while(True):
			# last packet received
			time_of_last_hit = self.sniffer_obj.traffic_queue[-1:] 
			start_time_of_traffic_eval = datetime.now() - timedelta(seconds=120)

			# store in taffic queue only urls hit during the last 2 minutes
			self.sniffer_obj.traffic_queue = [i for i in self.sniffer_obj.traffic_queue if i[0] >= start_time_of_traffic_eval]
			#no. of hits in last two minutes
			traffic_last_two_mins = len(self.sniffer_obj.traffic_queue)
			#print(self.sniffer_obj.traffic_queue)

			if(traffic_last_two_mins > self.avg_hits):
				#self.generate_high_traffic_alert(traffic_last_two_mins, time_of_last_hit[0])
				self.high_traffic_flag = True
				self.recovered_flag = False
				self.alert_time =  time_of_last_hit[0][0]
				self.traffic_at_alert_time = traffic_last_two_mins

			elif (self.high_traffic_flag and traffic_last_two_mins < self.avg_hits):
				self.high_traffic_flag = False
				#self.generate_recovered_high_traffic_alert(time_of_last_hit[0])
				self.alert_recovery_time = datetime.now()
				self.recovered_flag = True
			time.sleep(30)

