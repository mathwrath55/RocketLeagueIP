# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 23:35:24 2022

@author: u/mathwrath55
Program searches Rocket League's log files and scans the location of the IP addresses
glob and requests modules may need to be installed
IP lookup API found at https://www.freecodecamp.org/news/how-to-get-location-information-of-ip-address-using-python/
"""
import glob
import requests

def get_location(ip):
    ip_address = ip
    response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
    location_data = {
        "ip": ip_address,
        "city": response.get("city"),
        "region": response.get("region"),
        "country": response.get("country_name")
    }
    return location_data

#replace the part in square brackets with the file address of the relevant folder
#for me, it was in C:/Users/(my user)/Documents/
file_dir = '[replace this part]/My Games/Rocket League/TAGame/Logs/'
file_names = sorted(glob.glob(file_dir+'*.log'))
for f in file_names:
    file = open(f, 'r')
    lines = file.read().split('\n')
    for l in lines:
        if 'RECV first packet' in l: #these lines have an easily accessible IP address and match IPs one-for-one
            try:
                ip = l.split(':')[1].split('=')[1]
                loc_data = get_location(ip)
                print(loc_data["ip"] + ": " + loc_data["city"] + ', ' + loc_data["region"] + ', ' + loc_data["country"])
            except Exception:
                continue
