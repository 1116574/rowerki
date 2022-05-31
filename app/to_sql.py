import json
import sqlite3


con = sqlite3.connect('data/bike_matrix.db')
cur = con.cursor()

with open('data/stations.json', 'r') as f:
    stations = json.load(f)

with open('data/resp.json', 'r') as f:
    table = json.load(f)

# Duration matrix

## Create table with columns for every station
ids = ['id']
for st in stations:
    ids.append(st['station_id'])

cur.execute(f'''CREATE TABLE durations {str(tuple(ids))}''', )

for i, row in enumerate(table["durations"]):
    first = stations[i]['station_id']
    row = [first] + row
    # print(f"INSERT INTO durations VALUES {str(tuple(row))}")
    cur.execute(f"INSERT INTO durations VALUES {str(tuple(row))}")

con.commit()

# Distance matrix
ids = ['id']
for st in stations:
    ids.append(st['station_id'])

cur.execute(f'''CREATE TABLE distances {str(tuple(ids))}''', )

for i, row in enumerate(table["distances"]):
    first = stations[i]['station_id']
    row = [first] + row
    # print(f"INSERT INTO distances VALUES {str(tuple(row))}")
    cur.execute(f"INSERT INTO distances VALUES {str(tuple(row))}")

con.commit()


# Station info
station_table = []
for st in stations:
    if st['name'].startswith('E-bike'):
        type = 'electric'
    elif st['name'].startswith('Veturilko'):
        type = 'kids'
    else:
        type = 'normal'

    station_table.append((st['station_id'], st['name'], st['short_name'], st['lat'], st['lon'], type, st['region_id'], st['capacity']))

cur.execute(f'''CREATE TABLE stations (id, name, short, lat, lon, type, region, capacity)''', )
cur.executemany(f"INSERT INTO stations VALUES (?,?,?,?,?,?,?,?)", station_table)

con.commit()
con.close()

