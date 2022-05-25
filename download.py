import json
import os
import requests

systems = [
    'nextbike_vp',  # Warszawa/Warsaw
    'nextbike_or',  # Otwock
    'nextbike_pi',  # Piaseczno
    'nextbike_os',  # Otwock
    'nextbike_gp',  # Grodzisk Mazowiecki
]

# This file downloads, splits, and preporccesses data from nextbike

# Max distance (in km) between two stations (optimization for routing)
KM_THRESHOLD = 10

stations = []
if not os.path.exists('data/stations.json'):
    for system in systems:
        print(f'Downloading {system}...')
        _system = requests.get(f'https://gbfs.nextbike.net/maps/gbfs/v2/{system}/pl/station_information.json').json()
        stations += _system['data']['stations']
    
    with open('data/stations.json', 'w') as f:
        json.dump(stations, f, indent=2)
else:
    with open('data/stations.json', 'r') as f:
        stations = json.load(f)


def distance(lat1, lon1, lat2, lon2):
    """Calculate distance beetwen 2 points given in lat-lon"""

    # src: https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude

    from math import sin, cos, sqrt, atan2, radians

    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(float(lat1))
    lon1 = radians(float(lon1))
    lat2 = radians(float(lat2))
    lon2 = radians(float(lon2))

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance

latlon = {}
optimized_matrix = []
for station in stations:

    id = station['station_id']
    lat = station['lat']
    lon = station['lon']
    latlon[id] = (lat, lon)
    close = []
    for station2 in stations:
        id2 = station2['station_id']
        lat2 = station2['lat']
        lon2 = station2['lon']
        
        abs_dist = distance(lat, lon, lat2, lon2)
        if abs_dist < KM_THRESHOLD:
            close.append(id2)

    optimized_matrix.append({'id': id, 'close': close})

with open('data/matrix.json', 'w') as f:
    json.dump(optimized_matrix, f, indent=2)

with open('data/gps.json', 'w') as f:
    json.dump(latlon, f, indent=2)
