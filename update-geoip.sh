#!/usr/bin/env bash

URL=http://geolite.maxmind.com/download/geoip/database/GeoLiteCountry/GeoIP.dat.gz
DST=$(dirname $0)/GeoIP.dat

curl $URL | gunzip > $DST
