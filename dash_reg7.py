import logging
import requests
import time

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

from scapy.all import *

MAGIC_FORM_URL = 'http://api.cloudstitch.com/kedar028/magic-form/datasources/sheet'

def record_poop():
  data = {
    "FirstName": time.strftime("%Y-%m-%d %H:%M"), 
    "LastName": 'Poopy Diaper'
  }
  requests.post(MAGIC_FORM_URL, data)

  print "SHOULD BE DONE"

def record_wake():
  data = {
    "Timestamp": time.strftime("%Y-%m-%d %H:%M"), 
    "Measurement": 'Woke from Sleep'
  }
  requests.post(MAGIC_FORM_URL, data)

def arp_display(pkt):
  timestamp = time.strftime("%Y-%m-%d %H:%M")
  if pkt[ARP].op == 1: #who-has (request)
    if pkt[ARP].psrc == '0.0.0.0': # ARP Probe
      if pkt[ARP].hwsrc == '10:ae:60:96:da:68': # Huggies        
        print "Pushed COOOOTTTTTTOOOON"
        record_poop()
      elif pkt[ARP].hwsrc == '10:ae:60:00:4d:f3': # Elements
        print "Pushed Elements"
        record_wake()
      else:
        print "ARP Probe from unknown device: " + pkt[ARP].hwsrc

print sniff(prn=arp_display, filter="arp", store=0, count=10)
 