#!/bin/bash

# change directory
cd /home/jan/Uni/DS-Project/data/Maps/

# download data to data/maps folder
wget -O "Bundeskarte.geojson" "https://raw.githubusercontent.com/isellsoap/deutschlandGeoJSON/main/1_deutschland/1_sehr_hoch.geo.json"
wget -O "Laenderkarte.geojson" "https://raw.githubusercontent.com/isellsoap/deutschlandGeoJSON/main/2_bundeslaender/1_sehr_hoch.geo.json"
wget -O "Kreiskarte.geojson" "https://raw.githubusercontent.com/isellsoap/deutschlandGeoJSON/main/4_kreise/1_sehr_hoch.geo.json"
wget -O "Staedte.geojson" "https://raw.githubusercontent.com/drei01/geojson-world-cities/master/cities.geojson"