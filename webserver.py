from flask import Flask
import sqlite3
from flask import g

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


if __name__ == "__main__":
    app.run(host='localhost', port=8080)


