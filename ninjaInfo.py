#!/usr/bin/python3
import os
import platform
import sys
import time
import requests
import socket
from icmplib import traceroute
import nmap

if platform.system() == 'Linux':
	os.system('clear')

if platform.system() == 'Windows' or platform.system() == 'windows':
	os.system('cls')

print("""
          _             _           ___            __         
  _ __   (_)  _ __     (_)   __ _  |_ _|  _ __    / _|   ___  
 | '_ \\  | | | '_ \\    | |  / _` |  | |  | '_ \\  | |_   / _ \\ 
 | | | | | | | | | |   | | | (_| |  | |  | | | | |  _| | (_) |
 |_| |_| |_| |_| |_|  _/ |  \\__,_| |___| |_| |_| |_|    \\___/ 
                     |__/                                     
""")
print('-'*72)
def usage():
	print("USAGE : sudo python3 ninjaInfo.py <IP>")

if len(sys.argv) != 2:
	usage()	

def geolocate_osint(target_ip):
	print("[*] doing this task with both port scanning and traceroute on target %s" % (target_ip))
	
	try:
		geo_locate = requests.get("http://ip-api.com/json/"+target_ip)
		js = geo_locate.json()

		status = js['status']
		country = js['country']
		country_code = js['countryCode']
		region = js['region']
		regionName = js['regionName']
		city = js['city']
		latitude = js['lat']
		longitude = js['lon']
		isp = js['isp']
		org = js['org']
		postal_code_PIN_code = js['zip']

		print('-'*72+'\n')
		print("""
------------------------------------------------------------------------
###################################
#      finding geolication        #
###################################""")
		print("[*] finding geolication with some usefull stuff about %s" % (target_ip))
		time.sleep(.6)
		print("|")
		print("|COUNTRY      : %s" % country)
		print("|COUNTRY_CODE : %s" % country_code)
		print("|REGION_NAME  : %s" % regionName)
		print("|REGION       : %s" % region)
		print("|CITY         : %s" % city)
		print("|LATITUDE TO LOCATION : %s" % latitude)
		print("|LONGITUDE TO LOCATION : %s" % longitude)
		print("|ISP of the device : %s" % isp)
		print("|ORG of the device : %s" % org)
		print("|PIN_CODE     : %s" % postal_code_PIN_code)
		print("-"*72)

	except:
		print("[!] Exception exists. ")

def tracert(target_ip):
	print("""
-----------------------------------------------------------------------
###########################
#       traceroute        #
###########################""")
	try:
		hops = traceroute(target_ip)
		print('Distance/TTL\tAddress\tAverage round-trip time')

		last_distance = 0

		for hop in hops:
			if last_distance +1 != hop.distance:
				print("***********something is wrong***********")

			print(f'{hop.distance}\t{hop.address}\t{hop.avg_rtt} ms')
			last_distance = hop.distance

	except:
		print("[-] sorry, make sure you are root!")

def os(target_ip):
	print("""
-----------------------------------------------------------------------
#######################
#    OS detection     #
#######################""")
	nm = nmap.PortScanner()
	x = nm.scan(hosts=target_ip, arguments='-O')

	scan_accuracy = nm[target_ip]['osmatch'][0]['accuracy']
	os_type = nm[target_ip]['osmatch'][0]['osclass'][0]['type']
	os_name = nm[target_ip]['osmatch'][0]['name']
	os_vendor = nm[target_ip]['osmatch'][0]['osclass'][0]['vendor']
	os_generation = nm[target_ip]['osmatch'][0]['osclass'][0]['osgen']
	os_family = nm[target_ip]['osmatch'][0]['osclass'][0]['osfamily']

	print('[+] found OS of the target with possible OS fingerprints')
	print('|')
	print('|OS type : %s' % (os_type))
	print('|scan accuracy : %s' % (scan_accuracy))
	print('|OS name : %s' % (os_name))
	print('|OS vendor : %s' % (os_vendor))
	print('|OS generation : %s' % (os_generation))
	print('|OS family : %s' % (os_family))
	print('-'*72+'\n')

	time.sleep(.2)

	print("""
-----------------------------------------------------------------------
##########################
#      port scanning     #
##########################""")
	print("[*] scanning for open ports")
	print("|")

	all_protocols = x['scan'][target_ip].all_protocols()[0]

	ports = list(x['scan'][target_ip][all_protocols])

	for open_ports in ports:
		port_status = x['scan'][target_ip][all_protocols][open_ports]['state']
		port_name = x['scan'][target_ip][all_protocols][open_ports]['name']

		print("PORT : %d         SERVICE : %s         STATUS : %s" % (open_ports,port_name,port_status))

if len(sys.argv) == 2 or len(sys.argv) == 4:
	target = sys.argv[1]
	resolved_target = socket.gethostbyname(target)

	system = platform.system()
	version = platform.version()
	os_version = version[1::]
	processor = platform.processor()

	print("[*] performing this task on %s %s with %s processor" % (system, os_version, processor))

	geolocate_osint(resolved_target)
	print(chr(0xa))
	tracert(resolved_target)
	print('-'*72)
	print(chr(0xa))
	os(resolved_target)