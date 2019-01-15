from threading import Thread
import time

class Display(Thread):

	

	def __init__(self, url_counter):
		super(Display, self).__init__()
		self.url_path_counter = url_counter

	def run(self):
		self.display_most_hits()

	def display_most_hits(self):
		while(True):
			#print url_path_counter
			if len(self.url_path_counter) > 0:
				#sorted_traffic = sorted(url_dict.items(), key=operator.itemgetter(1), reverse=True)[:10]
				sorted_traffic = sorted(self.url_path_counter.items(), key=self.url_path_counter.get, reverse=True)[0:3]
				print "\n\n-------------------------------------------------Network Traffic -------------------------------------------------"
				print "------------------------------------------------------------------------------------------------------------------"
				print "                                                  Most URL Hits                                                   "
				print "------------------------------------------------------------------------------------------------------------------"
				print "------------------------------------------------------------------------------------------------------------------"
				for key,value in sorted_traffic:
					print "{:64s}:{:50d}".format(key,value)
				print "------------------------------------------------------------------------------------------------------------------\n"
			time.sleep(10)