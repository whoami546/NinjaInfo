#!/usr/bin/python3
from requests import get
from socket import gethostbyname
from pyfiglet import figlet_format
from sys import argv
from hashlib import md5
from re import findall
import argparse

parser = argparse.ArgumentParser(
	description="NinjaInfo, a OSINT tool which can be used by every OSINT investigators.",
	epilog="Example - %(prog)s --geolocate-ip 49.37.64.197 --scrap-mail https://www.google.com"
)
parser.add_argument(
		"--geolocate-ip", 
		help="Geolocate by IPv4 public address given by user", 
		dest="ip_address", 
		nargs=1
		)
parser.add_argument(
		"--geolocate-phone",
		help="Geolocate by Phone Number given by user (e.g. : python3 %(prog)s --geolocate-phone +917209839773 )",
		dest="phone_number",
		nargs=1
		)
parser.add_argument(
		"--scrap-mail", 
		help="Only use it for scraping mail from a website or platform.", 
		dest="scrap_mail", 
		nargs=1
		)
parser.add_argument(
		"--getby-favicon",
		help="Do tell the framework used by the website by just using the favicon.ico's path.",
		dest="favicon",
		nargs=1
		)
parser.add_argument(
		"--version",
		help="print version",
		action="version",
		version="%(prog)s 1.0",
)

argument = parser.parse_args()

try:
	from phonenumbers import geocoder, parse, timezone, carrier
except Exception as e:
	print(e)
	exit(0)

if len(argv) == 1:
	parser.print_help()
	exit(0)

print(figlet_format("NinjaInfo"))
print("\t"*3 + "-by twitter:whoamiPwns, Github:@whoami546\n")

def parsePhonedo(number):
	flag = 0
	phoneNumber = parse(number)
	if phoneNumber:
		print(f"\n\033[1;34m[\033[1;36m+\033[1;34m]\033[0m {phoneNumber}")
		location = geocoder.description_for_number(phoneNumber, lang="en")
		service_provider = carrier.name_for_number(phoneNumber, lang="en")
		TimeZone = timezone._country_level_time_zones_for_number(phoneNumber)
		if location:
			print(f"\033[1;34m[\033[1;36m+\033[1;34m]\033[0m Location for Phone Number : {location}")
			if service_provider:
				print(f"\033[1;34m[\033[1;36m+\033[1;34m]\033[0m service provider for number : {service_provider}")
			if TimeZone:
				print(f"\033[1;34m[\033[1;36m+\033[1;34m]\033[0m Timezone for number : {TimeZone[0]}")
		try:
			from opencage.geocoder import OpenCageGeocode
			key = "abcfabed23174112b3d7b6c93ed7a5b2"
			loc = OpenCageGeocode(key)
			flag = loc.geocode(location)[0]

		except Exception as e:
			pattern = findall(r"^.{9}.{14}", str(e))
			print(f"\n\033[0;31m[ERROR] {pattern[0]}")
			print("[ERROR] geolocation with phonenumber terminated !\033[0m")
		else:
			pass
	else:
		pass
	return flag

def geolocatePhone(number):
	print("\033[1;33m"+"="*23+"[Geolocate Phone Number]"+"="*23+"\033[0m")
	try:
		value_flag = parsePhonedo(number)
		if value_flag != 0:
			geometery = value_flag.get("geometry")
			annotations = value_flag.get("annotations")
			if annotations != None:
				mgrs = annotations.get("MGRS")
				print(f"\033[1;34m[\033[1;36m+\033[1;34m]\033[0m MGRS : {mgrs}")

			if geometery != None:
				latitude = geometery.get("lat")
				longitude = geometery.get("lng")
				print(f"\033[1;34m[\033[1;36m+\033[1;34m]\033[0m latitude : {latitude}")
				print(f"\033[1;34m[\033[1;36m+\033[1;34m]\033[0m longitude : {longitude}")

	except Exception as e:
		err = findall(r"^.{9}.{14}", str(e))
		print(f"\n\033[0;31m[ERROR] {err}\033[0m")
	print("\n\033[1;33m"+"="*23+"="*24+"="*23+"\033[0m")

def resolve_ip(target_ip):
	try:
		target = ''.join(target_ip.split())
		if target.count('.') > 0:
			ip = gethostbyname(target)
		return ip
	except:
		return 0

def geolocateIP(ip_addr):
	try:
		request = get(f"http://ip-api.com/json/{ip_addr}")
		data = request.json()
		return data
	except Exception as e:
		return e

def geolocateMainIP(public_ip):
	print("\n\033[1;33m"+"="*23+"[Geolocate IPv4 address]"+"="*23+"\033[0m\n")
	try:
		ip = resolve_ip(public_ip)
		if not ip:
			print("\033[0;31m[ERROR] can't resolve the given host to IPv4 address\033[0m\n")
		else:
			result = geolocateIP(ip)
			if result['status'] == 'success':
				for x in result:
					print(f"\033[1;34m[\033[1;36m+\033[1;34m]\033[0m {x} : {result.get(x)}")
			else:
				print("\033[0;31m[ERROR] Expected a public IP..?!\033[0m")
	except Exception as e:
		raise e
	print("\n\033[1;33m"+"="*23+"="*24+"="*23+"\033[0m")

def favICON(path):
	try:
		secure_path = findall(r"", path)
	except:
		pass

