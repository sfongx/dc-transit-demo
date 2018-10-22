from django.core import serializers

from .abstractTransit import AbstractTransit
from ..models import Agency, Stops, Routes, Trips, Calendar, StopTimes

from datetime import datetime, time, timedelta
from dateutil import tz

import json, functools, logging

def vehicleCMP(vehicle1, vehicle2):
    # Sorting function for vehicle's minutes
    # IMPORTANT: Not defined as a class method
    time1 = vehicle1['minutes']
    time2 = vehicle2['minutes']

    return time1 - time2

class GtfsGeneric(AbstractTransit):
    def __init__(self, agencyId):
        # Grab the agency in question from database
        self.agency = Agency.objects.get(pk = agencyId)

        # Get the agency's timezone, current time, and current day of the week
        self.timezone = tz.gettz(self.agency.time_zone)
        self.currentTime = datetime.now(self.timezone)
        self.dayOfWeekNum = self.currentTime.weekday()

        # Get agency's calendar info
        self.calendarInfo = self.getCalendarInfo()

        # Create a list with names of the week in order
        self.dayOfWeekMap = ['monday', 'tuesday', 'wednesday',
            'thursday', 'friday', 'saturday', 'sunday']

        # Test time
        # self.currentTime = datetime(2018, 10, 18, 23, 45, 5, 00000, tzinfo=self.timezone)

    def getStopTimesAtStop(self, stopId):
        # Query stops times for all trips at this stop
        allTripsAtStop = StopTimes.objects.filter(agency = self.agency, stop_id = stopId)

        logger = logging.getLogger(__name__)

        if allTripsAtStop:
            # If query succeeded, proceed to...

            # Get timestamp for 60 minutes from now
            limitTstamp = self.currentTime + timedelta(minutes=60)

            if limitTstamp.hour < self.currentTime.hour:
                # Time overflows to the next day

                # First range: Everything till end of the day
                firstStart = time(self.currentTime.hour, self.currentTime.minute, self.currentTime.second)
                firstEnd = time.max

                # Query the first range. Convert to JSON and then to dict
                firstTripsQuery = allTripsAtStop.filter(arrival_time__range=(firstStart, firstEnd))
                firstTripsJson = serializers.serialize("json", firstTripsQuery)
                firstTripsDict = json.loads(firstTripsJson)

                # Second range: Start of next day until the limit
                secondStart = time.min
                secondEnd = time(limitTstamp.hour, limitTstamp.minute, limitTstamp.second)

                # Query the second range. Convert to JSON and then to dict
                secondTripsQuery = allTripsAtStop.filter(arrival_time__range=(secondStart, secondEnd))
                secondTripsJson = serializers.serialize("json", secondTripsQuery)
                secondTripsDict = json.loads(secondTripsJson)

                # Combine the two and return
                combined = firstTripsDict + secondTripsDict

                return combined

            else:
                # Normal case

                # Create datetime.time objects for the request timestamp and the limit timestamp
                requestTime = time(self.currentTime.hour, self.currentTime.minute, self.currentTime.second)
                timeLimit = time(limitTstamp.hour, limitTstamp.minute, limitTstamp.second)

                # Filter the trips at the stop within the next hour and convert to JSON
                closestTripsQuery = allTripsAtStop.filter(arrival_time__range=(requestTime, timeLimit))
                closestTripsJson = serializers.serialize("json", closestTripsQuery)

                logger.debug("Combined: %s", closestTripsJson)

                # Return as dict
                return json.loads(closestTripsJson)

        else:
            # Return false if the stop ID isn't valid
            return False

    def getCalendarInfo(self):
        # Get and convert the query for calendar info filtering by agency
        calendarQuery = Calendar.objects.filter(agency = self.agency)
        calendarJson = serializers.serialize("json", calendarQuery)
        calendarDict = json.loads(calendarJson)

        # Return the resultant dict
        return calendarDict

    def calendarCheck(self, tripInfo):
        # Given a trip's service ID determine if it runs today
        for entry in self.calendarInfo:
            item = entry['fields']
            if item['service_id'] == tripInfo['service_id']:
                # Once a matching service ID is found, check day of week
                if item[self.dayOfWeekMap[self.dayOfWeekNum]] == 1:
                    # Return true if service runs today (indicated by binary 1)
                    return True
                else:
                    # Return false if not (indicated by binary 0)
                    return False

        # If nothing found return false just in case
        return False

    def getStopInfo(self, stopId):
        # Get and convert the query for stop info filtering by agency and stop ID
        stopsQuery = Stops.objects.filter(agency = self.agency, stop_id = stopId)
        stopsJson = serializers.serialize("json", stopsQuery)
        stopsDict = json.loads(stopsJson)

        # Initialize blank dict to return
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

        # Initialize blank dict to return
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
        
        # Initialize blank dict to return
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

        for vehicle in response:
            # Get vehicle's trip data
            tripInfo = self.getTripInfo(vehicle['fields']['trip_id'])

            # Check to see if the trip runs today
            if (self.calendarCheck(tripInfo) == True):
                # If trip runs today, proceed to...

                # Get vehicle's route data
                routeInfo = self.getRouteInfo(tripInfo['route_id'])

                # Get the vehicle's arrival datetime
                arrivalTime = vehicle['fields']['arrival_time'].split(":")
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

            # Do nothing and do not add if trip does not run today

        # Outside loop once it's done grabbing and parsing predictions...

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
                'error': 'Stop ID %s is not valid or no service within the next hour' % stopId
            }
