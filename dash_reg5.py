#!/usr/bin/env python
import socket
import struct
import binascii

import time
import sys
import os
MAGIC_FORM_URL = 'http://api.cloudstitch.com/REPLACEME/magic-form/datasources/sheet'

# Written by Bob Steinbeiser (https://medium.com/@xtalker)
# Modded By Juan

def record_poop():
    data = {
        "Timestamp": time.strftime("%Y-%m-%d %H:%M"),
        "Measurement": 'Poopy Diaper'
    }
    requests.post(MAGIC_FORM_URL, data)


def record_wake():
    data = {
        "Timestamp": time.strftime("%Y-%m-%d %H:%M"),
        "Measurement": 'Alert'
    }
    requests.post(MAGIC_FORM_URL, data)


rawSocket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW,
                          socket.htons(0x0003))
MAC = '10:ae:60:96:da:68'
MACB = '111111111112'


while True:
    packet = rawSocket.recvfrom(2048)

    ethernet_header = packet[0][0:14]
    ethernet_detailed = struct.unpack('!6s6s2s', ethernet_header)

    arp_header = packet[0][14:42]
    arp_detailed = struct.unpack('2s2s1s1s2s6s4s6s4s', arp_header)

    # skip non-ARP packets
    ethertype = ethernet_detailed[2]
    if ethertype != '\x08\x06':
        continue

    source_mac = binascii.hexlify(arp_detailed[5])
    dest_ip = socket.inet_ntoa(arp_detailed[8])
    timestamp = time.strftime("%Y-%m-%d %H:%M")

    if source_mac == MAC:
        print "Dash button pressed!, IP = " + dest_ip
        record_poop()
	rawSocket.close()
	time.sleep(10)
	os.execl('/ENTERPATHHERE/dash-listen-X.py', '/ENTERPATHHERE/dash-listen-X.py')
    elif source_mac == MACB:
        print "Dash button 2 pressed!, IP = " + dest_ip
        record_wake()
	rawSocket.close()
        time.sleep(10)
	os.execl('/ENTERPATHHERE/dash-listen-X.py', '/ENTERPATHHERE/dash-listen-X.py')