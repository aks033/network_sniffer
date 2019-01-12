from scapy.all import IP
from scapy.all import sniff
from scapy.layers import http
import dpkt

# dictionary to keep a count of urls
url_dict = {}

def sniff_urls(packet):

	if packet.haslayer(http.HTTPRequest):
		http_layer = packet.getlayer(http.HTTPRequest)
		ip_layer = packet.getlayer(IP)
		#print '\n{0[src]} - {1[Method]} - http://{1[Host]}{1[Path]}'.format(ip_layer.fields, http_layer.fields)
		print http_layer.fields
		
		url_key = http_layer.fields["Host"]
		#print http_layer.fields["Path"], http_layer.fields["Path"].strip('/').split('/')

		path = http_layer.fields["Path"].strip('/').split('/')
		if(len(path) > 0):
			url_key = url_key + "/"+ path[0]
			if url_key not in url_dict:
				url_dict[url_key] = 1
			else:
				url_dict[url_key] = url_dict[url_key] + 1

		display_website_stats(url_dict)

def display_website_stats(url_dict):
	print url_dict

dev = 'enp0s3'
sniff(iface = dev, filter='tcp', prn=sniff_urls)