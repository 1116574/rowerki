import json


with open('data/stations.json', 'r') as f:
    stations = json.load(f)

key_names = {}

for st in stations:
    key_names[st['station_id']] = st

with open('data/station_names.json', 'w') as f:
    json.dump(key_names, f)


