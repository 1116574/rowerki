# Vetu-router
Router for Warsaw's public bike system (Veturilo) that splits every journey into sub 20 min legs, in order to be eligable for free tier of renting.

## Available endpoints
- `/dijkstra/<id1>/<id2>` a route between 2 stations
- `/<id1>` all stations within 20 min of `id1`
- `/closest/<lat>/<lon>` util for getting closest station to your location

There is also a very simplistic web interface at `/static/router.html` and `/static/map.html`

## Usage
1. `download.py` this downloads GBFS data
2. `osrm_matrix.py` with running OSRM server, see [this file for instructions](osrm.md)
3. `to_sql.py` to create database
4. OPTIONAL `to_name_keys.py` for webapp use, not required by API


## Data sources

### 20 mins free used here
GBFS: `https://gbfs.nextbike.net/maps/gbfs/v2/nextbike_vp/pl/station_information.json`
- `nextbike_vp` [Warszawa](https://gbfs.nextbike.net/maps/gbfs/v2/nextbike_vp/pl/station_information.json) -new api-
- `nextbike_or` [Pruszków](https://api.nextbike.net/maps/gbfs/v1/nextbike_or/gbfs.json)
- `nextbike_pi` [Piaseczno](https://api.nextbike.net/maps/gbfs/v1/nextbike_pi/gbfs.json)
- `nextbike_os` [Otwock](https://api.nextbike.net/maps/gbfs/v1/nextbike_os/gbfs.json)
- `nextbike_gp` [Grodzisk Mazowiecki](https://api.nextbike.net/maps/gbfs/v1/nextbike_gp/gbfs.json)

### 30 mins free, not used here, but may be useful to you
- `nextbike_zy` [Żyrardów](https://api.nextbike.net/maps/gbfs/v1/nextbike_zy/gbfs.json)