from django.core import serializers

from .abstractTransit import AbstractTransit
from ..models import Agency, Stops, Routes, Trips, StopTimes

from datetime import datetime, time, timedelta
from dateutil import tz

import json, logging, math

class GtfsGeneric(AbstractTransit):
    def __init__(self, agencyId):
        # Grab the agency in question from database
        self.agency = Agency.objects.get(pk = agencyId)

        # Get the agency's timezone and current time
        self.timezone = tz.gettz(self.agency.time_zone)
        self.currentTime = datetime.now(self.timezone)

    def getTripsAtStop(self, stopId):
        # Get the trips for this stop
        allTripsAtStop = StopTimes.objects.filter(agency = self.agency, stop_id = stopId)

        # Get timestamp for 90 minutes from now
        limitTstamp = self.currentTime + timedelta(minutes=60)

        # Create datetime.time objects for the request timestamp and the limit timestamp
        requestTime = time(self.currentTime.hour, self.currentTime.minute, self.currentTime.second)
        timeLimit = time(limitTstamp.hour, limitTstamp.minute, limitTstamp.second)

        # Filter the trips at the stop within the next 90 minutes
        closestTrips = allTripsAtStop.filter(arrival_time__range=(requestTime, timeLimit))

        closestTripsJson = serializers.serialize("json", closestTrips)

        return json.loads(closestTripsJson)

    def getStopInfo(self, stopId):
        # Get and convert the query set filtering by the agency and stop ID
        stopsQuery = Stops.objects.filter(agency = self.agency, stop_id = stopId)
        stopsJson = serializers.serialize("json", stopsQuery)
        stopsDict = json.loads(stopsJson)

        # Initialize a blank dict
        out = {}

        # Start loop but assumes a stop ID is unique for every agency
        for stop in stopsDict:
            out = stop['fields']
            break

        return out

    def getTripInfo(self, tripId):
        # Get and convert the query set filtering by the agency and trip ID
        tripsQuery = Trips.objects.filter(agency = self.agency, trip_id = tripId)
        tripsJson = serializers.serialize("json", tripsQuery)
        tripsDict = json.loads(tripsJson)

        # Initialize a blank dict
        out = {}

        # Start loop but assumes a trip ID is unique for every agency
        for trip in tripsDict:
            out = trip['fields']
            break

        return out

    def getRouteInfo(self, routeId):
        # Get and convert the query set filtering by the agency and route ID
        routesQuery = Routes.objects.filter(agency = self.agency, route_id = routeId)
        routesJson = serializers.serialize("json", routesQuery)
        routesDict = json.loads(routesJson)
        
        # Initialize a blank dict
        out = {}

        # Start loop but assumes a route ID is unique for every agency
        for route in routesDict:
            out = route['fields']
            break

        return out


    def parseResponse(self, stopId, response):
        # Get stop info
        currentStop = self.getStopInfo(stopId)

        # Initial data with the name of the stop and agency
        parsedRepsonse = {
            'agencyName': self.agency.name,
            'stopName': currentStop['stop_name'],
            'predictions': []
        }

        logger = logging.getLogger(__name__)

        for train in response:
            # Get train's trip data
            tripInfo = self.getTripInfo(train['fields']['trip_id'])
            logger.debug("%s", json.dumps(train, indent=4))

            # Get train's route data
            routeInfo = self.getRouteInfo(tripInfo['route_id'])

            # Get the train's arrival datetime
            arrivalTime = train['fields']['arrival_time'].split(":")
            arrivalDatetime = datetime(self.currentTime.year,
                self.currentTime.month,
                self.currentTime.day,
                int(arrivalTime[0]),
                int(arrivalTime[1]),
                int(arrivalTime[2]),
                00000,
                tzinfo=self.timezone)

            # Calculate minutes away and round down
            tMinusDelta = arrivalDatetime - self.currentTime
            minutesAway = math.floor(tMinusDelta.seconds / 60)

            # Now put it all together
            parsedRepsonse['predictions'].append({
                'shortRoute': routeInfo['short_name'],
                'fullRoute': routeInfo['long_name'],
                'destination': "",
                'direction': "",
                'minutes': minutesAway,
                'vehicleId': tripInfo['trip_id']
            })

        return parsedRepsonse

    def getResponse(self, stopId):
        rawResponse = self.getTripsAtStop(stopId)

        return self.parseResponse(stopId, rawResponse)
