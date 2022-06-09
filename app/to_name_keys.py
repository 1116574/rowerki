import json

import os
print(os.getcwd())

with open('app/data/stations.json', 'r') as f:
    stations = json.load(f)

key_names = {}

for st in stations:
    key_names[st['station_id']] = st

with open('app/data/station_names.json', 'w') as f:
    json.dump(key_names, f)

# For front end
with open('app/static/station_names.js', 'w') as f:
    file = json.dumps(key_names)
    file = 'const station_names = ' + file
    f.write(file)


