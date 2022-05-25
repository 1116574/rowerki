import json
import requests
# OSRM lib doesnt seem to work on windows

with open('stations.json', 'r') as f:
    stations = json.load(f)

with open('gps.json', 'r') as f:
    gps = json.load(f)

full_list = ''
for station in gps:
    coord = f'{gps[station][1]},{gps[station][0]}'
    full_list += f'{coord};'

print(f'http://192.168.100.48:5000/table/v1/biking/{full_list[:-1]}?annotations=distance,duration')  # the -1 is for trailing ;

response = requests.get(f'http://192.168.100.48:5000/table/v1/biking/{full_list[:-1]}?annotations=distance,duration').json()
with open('resp.json', 'w') as f:
    json.dump(response, f, indent=2)
