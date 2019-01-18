import logging

class TrafficLog:
	def __init__ (self, file_name):
		logging.basicConfig(filename = file_name, level=logging.INFO)


	def log_info(msg_str):
		logging.info(msg_str)