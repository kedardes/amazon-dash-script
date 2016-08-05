import logging
import urllib2

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

from scapy.all import *

def record_poop():
  urllib2.urlopen("http://maker.ifttt.com/trigger/dashtest/with/key/cn2LbRu-F4KBymTiJ8KBEf").read()

def arp_display(pkt):
  timestamp = time.strftime("%Y-%m-%d %H:%M")
  if pkt[ARP].op == 1: #who-has (request)
    if pkt[ARP].psrc == '0.0.0.0': # ARP Probe
      if pkt[ARP].hwsrc == '10:ae:60:96:da:68': # Huggies        
        print "Pushed Huggies"
        record_poop()
      else:
        print "ARP Probe from unknown device: " + pkt[ARP].hwsrc

print sniff(prn=arp_display, filter="arp", store=0, count=10)