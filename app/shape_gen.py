import json
import requests
# OSRM lib doesnt seem to work on windows

with open('data/stations.json', 'r') as f:
    stations = json.load(f)

with open('data/gps.json', 'r') as f:
    gps = json.load(f)

pairs = []
for station in gps:
    coord = f'{gps[station][1]},{gps[station][0]}'
    for station2 in gps:
        coord2 = f'{gps[station2][1]},{gps[station2][0]}'
        pairs.append([station, station2, coord, coord2])

# print(f'http://192.168.100.48:5000/route/v1/biking/{full_list[:-1]}')

successes = 0
for pair in pairs:
    mem = {}
    print(pair)
    print(f'http://192.168.100.48:5000/route/v1/biking/{pair[2]};{pair[3]}?geometries=geojson')
    response = requests.get(f'http://192.168.100.48:5000/route/v1/biking/{pair[2]};{pair[3]}?geometries=geojson').json()
    if response['code'] == 'Ok':
        successes += 1
        mem[f'{pair[0]} -> {pair[1]}'] = response['routes'][0]['geometry']['coordinates']
    else:
        print('Error', response['code'])

    if successes % 100 == 0:
        with open('data/shapes.json', 'w') as f:
            json.dump(mem, f, indent=2)
