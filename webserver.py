import json

from flask import Flask
import sqlite3
from flask import g
from flask import Response

from dijkstra import dijkstra

app = Flask(__name__)

DATABASE = 'data/bike_matrix.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def get_locations():
    gps = getattr(g, '_gps', None)
    if gps is None:
        with open('data/gps.json', 'r') as f:
            gps = g._gps = json.load(f)
    return gps

def get_station_names():
    station_names = getattr(g, '_station_names', None)
    if station_names is None:
        with open('data/station_names.json', 'r') as f:
            station_names = g._station_names = json.load(f)
    return station_names

def get_graph():
    graph = getattr(g, '_graph', None)
    if graph is None:
        from dijkstra import create_graph
        with open('data/stations.json', 'r') as f:
            stations = json.load(f)

        with open('data/resp.json', 'r') as f:
            durations = json.load(f)['durations']

        # graph = {"node1": {"node2": weight, ...}, ...}
        graph = create_graph(stations, durations)
        g._graph = graph
    return graph


def distance(lat1, lon1, lat2, lon2):
    """Calculate distance beetwen 2 points given in lat-lon"""
    # src: https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude
    from math import sin, cos, sqrt, atan2, radians

    # approximate radius of earth in km
    R = 6373.0

    try:
        lat1 = radians(float(lat1))
        lon1 = radians(float(lon1))
        lat2 = radians(float(lat2))
        lon2 = radians(float(lon2))
    except ValueError:
        return -1

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c

    return distance


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/<int:id>")
def get_stations(id):
    db = get_db()
    c = db.cursor()
    # fuck it
    # For normal cyclist (~18 min)
    # query = f'SELECT id, "{id}" FROM durations WHERE "{id}" < 1100'
    # c.execute(query)
    # result = c.fetchall()
    # normal = []
    # for entry in result:
    #     response = {}
    #     response['id'] = entry[0]
    #     response['duration'] = entry[1]
    #     normal.append(response)

    # EXTREEEEME CYCLING (hard 20 min)
    query = f'SELECT id, "{id}" FROM durations WHERE "{id}" < 1200'
    c.execute(query)
    result = c.fetchall()
    extreme = []
    for entry in result:
        response = {}
        response['id'] = entry[0]
        response['duration'] = entry[1]
        extreme.append(response)
    
    return {'results': extreme}


@app.route("/closest/<float:lat1>,<float:lon1>")
def closest(lat1, lon1):
    print(lat1, lon1)
    gps = get_locations()
    all_distances = []
    for stat in gps:
        lat2 = gps[stat][0]
        lon2 = gps[stat][1]
        dist = distance(lat1, lon1, lat2, lon2)
        all_distances.append((stat, dist))

    all_distances.sort(key=lambda tup: tup[1])
    return {'closest': all_distances}


@app.route("/dijkstra/<int:id1>/<int:id2>")
def dijakstra(id1, id2):
    from dijkstra import dijkstra
    # Check those ids exist
    locations = get_locations()
    if (str(id1) in locations) and (str(id2) in locations):
        graph = get_graph()

        route = dijkstra(graph, str(id1), str(id2))
        if route is None:
            return Response('{"error": "No route found"}', status=404, mimetype='application/json')
        names = []
        time = 0
        durations = []
        step_by_step = []
        station_names = get_station_names()
        for i, id in enumerate(route):
            try:
                time += graph[id][route[i+1]]
                durations.append(graph[id][route[i+1]]/60)
                names.append(station_names[id]['name'])
                step_by_step.append(id)
                step_by_step.append(graph[id][route[i+1]])
            except IndexError:
                names.append(station_names[id]['name'])
                step_by_step.append(id)
        return {'time': time/60, 'route': route, 'durations': durations, 'names': names, 'step_by_step': step_by_step}
    else:
        return {'error': 400, 'TF1': (id1 in locations), 'TF2': (id2 in locations), 'loc': locations}

@app.route("/route/<float:lat1>,<float:lon1>/<float:lat2>,<float:lon2>")
def dummy(lat1, lon1, lat2, lon2):
    return None

if __name__ == "__main__":
    app.run(host='localhost', port=8080)


