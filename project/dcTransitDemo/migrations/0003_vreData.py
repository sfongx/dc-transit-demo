# Generated by Django 2.0.8 on 2018-09-25 02:55

from django.db import migrations
from ..models import Agency, Stops, Routes, Trips, StopTimes
from ..staticData.gtfsGeneric import GtfsGeneric
import datetime

import logging

def add_vre_data(apps, schema_editor):
    # Get the VRE Agency
    currentAgency = Agency.objects.get(pk='vre')

    # Get a new static parser object with the gtfs link
    staticParser = GtfsGeneric(currentAgency.gtfs_link)

    # Stop list
    stops = staticParser.parseStops()

    # Route list
    routes = staticParser.parseRoutes()

    # Trip list
    trips = staticParser.parseTrips()

    # Stop times list
    stopTimes = staticParser.parseStopTimes()

    # Make the parser object close the zip file
    staticParser.closeZip()

    # Get a logger
    logger = logging.getLogger(__name__)

    # Save the stops
    logger.debug("Saving stops...")
    for stop in stops:
        Stops(
            agency = currentAgency,
            stop_id = stop['stop_id'],
            stop_name = stop['stop_name'],
            lat = stop['lat'],
            lon = stop['lon']
            ).save()

    # Save the routes
    logger.debug("Saving routes...")
    for route in routes:
        Routes(
            agency = currentAgency,
            internal_agency_id = route['internal_agency_id'],
            route_id = route['route_id'],
            short_name = route['short_name'],
            long_name = route['long_name'],
            text_color = route['text_color'],
            background_color = route['background_color']
            ).save()

    # Save the trips
    logger.debug("Saving trips...")
    for trip in trips:
        Trips(
            agency = currentAgency,
            route_id = trip['route_id'],
            trip_id = trip['trip_id']
            ).save()

    # Save the stop times
    logger.debug("Saving stop times, this may take a long time...")
    for stopTime in stopTimes:
        StopTimes(
            agency = currentAgency,
            trip_id = stopTime['trip_id'],
            stop_id = stopTime['stop_id'],
            arrival_time = datetime.time(stopTime['arr_hour'], stopTime['arr_min'], stopTime['arr_sec']),
            departure_time = datetime.time(stopTime['dep_hour'], stopTime['dep_min'], stopTime['dep_sec'])
            ).save()


class Migration(migrations.Migration):

    dependencies = [
        ('dcTransitDemo', '0002_initialAgency'),
    ]

    operations = [
        migrations.RunPython(add_vre_data)
    ]
