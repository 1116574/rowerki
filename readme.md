# Vetu-router
## Creating data files
1. `download.py`
2. `osrm_matrix.py` with running osrm server
3. `to_sql.py`
4. `to_name_keys.py` for webapp


## Data sources

### 20 minutowe free/okolice wawy
GBFS: `https://gbfs.nextbike.net/maps/gbfs/v2/nextbike_vp/pl/station_information.json`
- `nextbike_vp` [Warszawa](https://gbfs.nextbike.net/maps/gbfs/v2/nextbike_vp/pl/station_information.json) -nowe api-
- `nextbike_or` [Pruszków](https://api.nextbike.net/maps/gbfs/v1/nextbike_or/gbfs.json)
- `nextbike_pi` [Piaseczno](https://api.nextbike.net/maps/gbfs/v1/nextbike_pi/gbfs.json)
- `nextbike_os` [Otwock](https://api.nextbike.net/maps/gbfs/v1/nextbike_os/gbfs.json)
- `nextbike_gp` [Grodzisk Mazowiecki](https://api.nextbike.net/maps/gbfs/v1/nextbike_gp/gbfs.json)

### 30 minutowe free
- `nextbike_zy` [Żyrardów](https://api.nextbike.net/maps/gbfs/v1/nextbike_zy/gbfs.json)