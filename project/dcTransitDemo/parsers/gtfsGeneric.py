from django.core import serializers

from .abstractTransit import AbstractTransit
from ..models import Agency, Stops, Routes, Trips, StopTimes

from datetime import datetime, time, timedelta
from dateutil import tz

import json, functools, logging

def vehicleCMP(vehicle1, vehicle2):
    # Sorting function for vehicle's minutes
    time1 = vehicle1['minutes']
    time2 = vehicle2['minutes']

    return time1 - time2

class GtfsGeneric(AbstractTransit):
    def __init__(self, agencyId):
        # Grab the agency in question from database
        self.agency = Agency.objects.get(pk = agencyId)

        # Get the agency's timezone and current time
        self.timezone = tz.gettz(self.agency.time_zone)
        self.currentTime = datetime.now(self.timezone)

        logger = logging.getLogger(__name__)
        logger.debug("Day of week: %s", self.currentTime.weekday())


    def getStopTimesAtStop(self, stopId):
        # Query stops times for all trips at this stop
        allTripsAtStop = StopTimes.objects.filter(agency = self.agency, stop_id = stopId)

        if allTripsAtStop:
            # If query succeeded, proceed to...

            # Get timestamp for 60 minutes from now
            limitTstamp = self.currentTime + timedelta(minutes=60)

            # Create datetime.time objects for the request timestamp and the limit timestamp
            requestTime = time(self.currentTime.hour, self.currentTime.minute, self.currentTime.second)
            timeLimit = time(limitTstamp.hour, limitTstamp.minute, limitTstamp.second)

            # Filter the trips at the stop within the next hour
            closestTrips = allTripsAtStop.filter(arrival_time__range=(requestTime, timeLimit))

            closestTripsJson = serializers.serialize("json", closestTrips)

            return json.loads(closestTripsJson)

        else:
            # Return false if the stop ID isn't valid
            return False

    def getStopInfo(self, stopId):
        # Get and convert the query for stop info filtering by agency and stop ID
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
        # Get and convert query for trip info (from the trips table) filtering by agency and trip ID
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
        # Get and convert query for route info filtering by agency and route ID
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
        parsedResponse = {
            'agencyName': self.agency.name,
            'stopName': currentStop['stop_name'],
            'predictions': []
        }

        # Blank list to put unsorted predictions
        unsortedPredictions = []

        for train in response:
            # Get train's trip data
            tripInfo = self.getTripInfo(train['fields']['trip_id'])

            # Get train's route data
            routeInfo = self.getRouteInfo(tripInfo['route_id'])

            # Get the train's arrival datetime (NEED TO CHANGE THIS FOR LATE NIGHT)
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
            rawTimeAway = arrivalDatetime - self.currentTime
            minutesAway = rawTimeAway.seconds // 60

            # Now put it all together
            unsortedPredictions.append({
                'shortRoute': routeInfo['short_name'],
                'fullRoute': routeInfo['long_name'],
                'destination': tripInfo['trip_headsign'],
                'direction': tripInfo['direction_id'],
                'minutes': minutesAway,
                'vehicleId': tripInfo['trip_id']
            })

        # Sort predictions by time
        sortedPredictions = sorted(unsortedPredictions, key=functools.cmp_to_key(vehicleCMP))

        # Put it into the main dict
        parsedResponse['predictions'] = sortedPredictions

        return parsedResponse

    def getResponse(self, stopId):
        rawResponse = self.getStopTimesAtStop(stopId)

        if rawResponse:
            return self.parseResponse(stopId, rawResponse)

        else:
            return {
                'error': 'Stop ID %s is not valid' % stopId
            }
