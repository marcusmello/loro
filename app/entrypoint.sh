#!/bin/sh

#echo "Waiting for Influx..."

#while ! nc -z $INFLUXDB_HOST $INFLUXDB_PORT; do
#    echo "Influx not read"
#    sleep 3
#done

#echo "Influx started"
exec poetry run loro