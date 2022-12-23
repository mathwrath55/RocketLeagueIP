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

def get_playlist(num):
    if num == 3:
        return 'Casual 3s'
    if num == 6:
        return 'Private Match'
    if num == 11:
        return 'Comp 2s'
    if num == 13:
        return 'Comp 3s'
    if num == 34:
        return 'Tourney 2s'
    if num == 38:
        return 'LTM'
    return 'Unknown (playlist ' + str(num) + ')'
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

#replace the path with your log folder
#for me, it was in C:/Users/(my user)/Documents/
file_dir = 'C:/Users/(my user)/Documents/My Games/Rocket League/TAGame/Logs/'
ip_lines = []
ips = []
serverRegions = []
playlists = []
cities = []
regions = []
countries = []

try:
    fileOld = open(file_dir + 'compiledIPs.csv', 'r')
    prev_ip_lines = fileOld.read().split('\n')
    for l in prev_ip_lines:
        if len(l) < 4:
            continue
        ip_lines.append(l)
        ips.append(l.split(';')[0].strip())
        serverRegions.append(l.split(';')[1].strip())
        playlists.append(l.split(';')[2].strip())
        cities.append(l.split(';')[3].strip())
        regions.append(l.split(';')[4].strip())
        countries.append(l.split(';')[5].strip())
except Exception:
    pass

file_names = sorted(glob.glob(file_dir+'*.log'))
for f in file_names:
    file = open(f, 'r')
    lines = file.read().split('\n')
    for l in lines:
        if 'Party: HandleServerReserved' in l: #these lines have an easily accessible IP address and match IPs one-for-one
            lineSections = l.split(',')
            sIP = ''
            sRegion = ''
            sPlaylist = ''
            for s in lineSections:
                if s[:6] == 'Region':
                    sRegion = s.split("\"")[1]
                if s[:8] == 'Playlist':
                    sPlaylist = s.split("=")[1]
                if s[:9] == 'BeaconURL':
                    sIP = s.split("\"")[1].split(":")[0]
            if len(sIP) > 4 and sIP not in ips:
                loc_data = get_location(sIP)
                ips.append(sIP)
                serverRegions.append(sRegion)
                playlists.append(sPlaylist)
                cities.append(loc_data["city"])
                regions.append(loc_data["region"])
                countries.append(loc_data["country"])
                
humanFormat = "{} ({}, {}): {}, {}, {}"
fileFormat = "{}; {}; {}; {}; {}; {}\n"
locationFormat = "({}) {}, {}, {}"
fullLocations = []
fileNew = open(file_dir + 'compiledIPs.csv', 'w')
for i in range(len(ips)):
    print(humanFormat.format(ips[i], serverRegions[i], get_playlist(int(playlists[i])), cities[i], regions[i], countries[i]))
    fileNew.write(fileFormat.format(ips[i], serverRegions[i], playlists[i], cities[i], regions[i], countries[i]))
    locHere = locationFormat.format(serverRegions[i], cities[i], regions[i], countries[i])
    if locHere not in fullLocations:
        fullLocations.append(locHere)
fileNew.close()
fullLocations.sort()
print()
print('Unique Location/Region Combinations:')
for l in fullLocations:
    print(l)
