from threading import Thread
import time
import os
from datetime import datetime, timedelta
from termcolor import colored

class Display(Thread):

	def __init__(self, sniffer, alerts):
		super(Display, self).__init__()
		self.sniffer = sniffer
		self.alerts = alerts
		self.avg_traffic_per_min_list = []

	def run(self):
		self.display_most_hits()

	def display_most_hits(self):
		'''Prints url information every 10 seconds'''

		os.system('cls' if os.name == "nt" else 'clear')
		while(True):

			#if len(self.sniffer.url_counter) > 0:
			#sorted_traffic = sorted(self.sniffer.url_counter.items(), key=self.sniffer.url_counter.get, reverse=True)[0:3]
			sorted_traffic = self.sniffer.url_counter.most_common(3)
			sorted_ip = self.sniffer.ip_list.most_common(3)
			start_time = datetime.now() - timedelta(seconds=60)
			traffic_per_min = len([i for i in self.sniffer.traffic_queue if i[0] >= start_time])
			self.avg_traffic_per_min_list.append(traffic_per_min) 
			os.system('cls' if os.name == "nt" else 'clear')
			print "\n\n-------------------------------------------------Network Traffic -------------------------------------------------"
			print "------------------------------------------------------------------------------------------------------------------"
			print "                                                     Most URL Hits                                               "
			print "------------------------------------------------------------------------------------------------------------------"
			print "------------------------------------------------------------------------------------------------------------------"
			for key,value in sorted_traffic:
				print "{:64s}:{}".format(key,value)
			print "------------------------------------------------------------------------------------------------------------------"
			print "------------------------------------------------------------------------------------------------------------------\n"
			print ("Most frequent IPs - "), 
			for ip in sorted_ip:
				print (ip[0 ] + " "),

			print "\nTraffic in the last minute - ", traffic_per_min
			print "Traffic rate (per minute) - ", sum(self.avg_traffic_per_min_list)/(len(self.avg_traffic_per_min_list)*1.0)
			print "\n\n\n"
			#print self.alerts.traffic_at_alert_time , self.alerts.alert_recovery_time
			if(self.alerts.alert_time != None):
				self.generate_high_traffic_alert(self.alerts.traffic_at_alert_time, self.alerts.alert_time)

			if(self.alerts.alert_recovery_time != None and self.alerts.alert_recovery_time > self.alerts.alert_time):
				self.generate_recovered_high_traffic_alert(self.alerts.alert_recovery_time)

			print "\n\nPress \"ctrl-c\" to exit"
			time.sleep(10)



	def generate_high_traffic_alert(self, url_hits, time_of_alert):
		''' Prints the high traffic alert message '''

		print colored("HIGH TRAFFIC GENERATED AN ALERT","red")
		print colored("URL HITS : {}".format(url_hits),"red")
		print colored("TRIGGERED AT : {}".format(time_of_alert),"red")


	def generate_recovered_high_traffic_alert(self, recovery_time):
		''' Prints the recovered traffic alert message '''

		print colored("\n\nRECOVERED FROM HIGH TRAFFIC AT {}".format(recovery_time), "green")