import json


with open('stations.json', 'r') as f:
    stations = json.load(f)['data']['stations']

key_names = {}

for st in stations:
    key_names[st['station_id']] = st

with open('station_names.json', 'w') as f:
    json.dump(key_names, f)


