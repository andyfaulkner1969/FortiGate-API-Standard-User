#!/usr/bin/env python3

import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

host = "10.10.90.1"
passwd = "XXXXXX"

def fgt_login():
	global host, passwd
	payload = {
		"username" : "andyf",
		"secretkey" : passwd
	}
	try:
		url = "https://" + host + "/api/v2/authentication" 
		fgt_login = requests.post(url, json= payload,verify=False)
		parsed_json = json.loads(fgt_login.text)
		print("Authenticated Successfully into the FGT. STATUS CODE: " + str(fgt_login.status_code))
		return fgt_login.cookies
	except:
		print("Something went wrong logging into the FGT: STATUS CODE: " + str(fgt_login.status_code))
	
def do_something(auth_cookies,url):
	global host
	try:
		url = "https://" + host + url
		api_task = requests.get(url, verify=False, cookies=auth_cookies)
		parsed_json = json.loads(api_task.text)
		print(json.dumps(parsed_json, indent=4, sort_keys=True))
	except:
		print("Something went wrong executing the requested URL on the FGT: STATUS CODE: " + str(api_task.status_code))

def fgt_logout(auth_cookies):
	global host
	try:
		url = "https://" + host + "/api/v2/authentication" 
		api_logout = requests.delete(url, verify=False, cookies=auth_cookies)
		print("Logged Out STATUS CODE: " + str(api_logout.status_code))
	except:
		print("Something went wrong logging out of the FGT: STATUS CODE: " + str(api_logout.status_code))

# Going to the FGT and getting the auth cookies. They are returned in the fgt_login function.
auth_cookies = fgt_login()
# Calling some function to achive on the FGT passing the auth cookies.
url = "/api/v2/monitor/system/current-admins"
do_something(auth_cookies,url)
# Let's be kind and log out.  Also passing the auth cookies.
fgt_logout(auth_cookies)