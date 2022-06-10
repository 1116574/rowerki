from fileinput import close
import json

from flask import Flask, jsonify, render_template
import sqlite3
from flask import g
from flask import Response

from dijkstra import dijkstra

app = Flask(__name__)

DATABASE = 'app/data/bike_matrix.db'

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
        with open('app/data/gps.json', 'r') as f:
            gps = g._gps = json.load(f)
    return gps

def get_station_names():
    station_names = getattr(g, '_station_names', None)
    if station_names is None:
        with open('app/data/station_names.json', 'r') as f:
            station_names = g._station_names = json.load(f)
    return station_names

def get_graph():
    graph = getattr(g, '_graph', None)
    if graph is None:
        from dijkstra import create_graph
        with open('app/data/stations.json', 'r') as f:
            stations = json.load(f)

        with open('app/data/resp.json', 'r') as f:
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
    return all_distances

def google_maps_url(route):
    waypoints = []
    for event in route:
        if event['type'] == 'journey':
            continue
        waypoints.append(str(event['lat']) + ',' + str(event['lon']))
        
    url = 'https://www.google.com/maps/dir/?api=1&origin=' + waypoints[0] + '&destination=' + waypoints[-1] + '&waypoints=' + ''.join(waypoints[1:-1])
    return url


### Endpoints

@app.route("/test")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/api/<int:id>")
def get_stations(id):
    db = get_db()
    c = db.cursor()

    # EXTREEEEME CYCLING (hard 20 min)
    query = f'SELECT id, "{id}" FROM durations WHERE "{id}" < 1200'  # its sanitazied by flask itself
    c.execute(query)
    result = c.fetchall()
    extreme = []
    for entry in result:
        response = {}
        response['id'] = entry[0]
        response['duration'] = entry[1]
        extreme.append(response)
    
    return {'results': extreme}

@app.route("/api/closest/<float:lat1>,<float:lon1>")
def closest_view(lat1, lon1):
    all_distances = closest(lat1, lon1)
    return jsonify(all_distances)

@app.route("/api/dijkstra/<int:id1>/<int:id2>")
def dijakstra(id1, id2):
    from dijkstra import dijkstra
    # Check those ids exist
    locations = get_locations()
    if (str(id1) in locations) and (str(id2) in locations):
        graph = get_graph()

        route = dijkstra(graph, str(id1), str(id2))
        if route is None:
            return Response('{"error": "No route found"}', status=404, mimetype='application/json')

        time = 0
        route_full = []
        route_simplified = []
        station_names = get_station_names()

        for idx in range(0, len(route)-1):
            current = route[idx]
            next = route[idx+1]
            t = graph[current][next]
            # simplified
            route_simplified.append(current)
            route_simplified.append(t)

            # full
            route_full += [{
                'type': 'station',
                'id': current,
                'name': station_names[current]['name'],
                'short_name': station_names[current]['short_name'],
                'lat': station_names[current]['lat'],
                'lon': station_names[current]['lon'],
            },
            {
                'type': 'journey',
                'duration': t,
                'distance': 0,
            }]
            time += t
        # last stop is skipped so we need to add it manually
        route_simplified.append(route[-1])
        route_full.append({
                'type': 'station',
                'id': next,
                'name': station_names[next]['name'],
                'short_name': station_names[next]['short_name'],
                'lat': station_names[next]['lat'],
                'lon': station_names[next]['lon'],
            })

        return {'total_time': time, 'route_full': route_full, 'route_simplified': route_simplified}
    else:
        # return {'error': 400, 'TF1': (id1 in locations), 'TF2': (id2 in locations), 'loc': locations}
        return Response('{"error": "Bike stations not found"}', status=404, mimetype='application/json')

@app.route("/api/route/<float:lat1>,<float:lon1>/<float:lat2>,<float:lon2>")
def complete_route(lat1, lon1, lat2, lon2):
    closest_1 = closest(lat1, lon1)[0][0]
    closest_2 = closest(lat2, lon2)[0][0]

    route = dijakstra(closest_1, closest_2)
    gmaps = google_maps_url(route['route_full'])

    return {**route, 'google_maps': gmaps}


### Views

@app.route("/route/<float:lat1>,<float:lon1>/<float:lat2>,<float:lon2>")
def route_view(lat1, lon1, lat2, lon2):
    closest1 = closest(lat1, lon1)[0]
    id1 = closest1[0]
    dist1 = closest1[1]

    closest2 = closest(lat2, lon2)[0]
    id2 = closest2[0]
    dist2 = closest2[1]

    route = dijakstra(id1, id2)
    gmaps = google_maps_url(route['route_full'])

    route = {**route, 'google_maps': gmaps}
    return render_template('router.html', route=route, walking=[dist1, dist2])

if __name__ == "__main__":
    app.run(host='localhost', port=80, debug=True)


