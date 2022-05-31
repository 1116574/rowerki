# Runinng OSRM
See [official project page for detailed instructions](https://github.com/Project-OSRM/osrm-backend)

1. Download region data from planet.osm
2. Run pre-proccessing commands:
```bash
docker run -t -v "${PWD}:/data" osrm/osrm-backend osrm-extract -p /opt/bicycle.lua /data/mazowieckie-latest.osm.pbf

docker run -t -v "${PWD}:/data" osrm/osrm-backend osrm-partition /data/mazowieckie-latest.osrm

docker run -t -v "${PWD}:/data" osrm/osrm-backend osrm-customize /data/mazowieckie-latest.osrm
```

3. Now you can run a server and make requests to it:
```bash
 #!/usr/bin/env bash
 docker run -t -i -p 5000:5000 -v "${PWD}:/data" osrm/osrm-backend osrm-routed --max-table-size 400 --algorithm mld /data/mazowieckie-latest.osrm
 ```

Note the table size