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

        # Get the agency's timezone and calendar info 
        self.timezone = tz.gettz(self.agency.time_zone)
        self.calendarInfo = self.getCalendarInfo()

        # Test time
        # self.currentTime = datetime(2018, 10, 18, 23, 45, 5, 00000, tzinfo=self.timezone)

        # Get the timezone aware current time and tomorrow with their days of the week
        self.currentTime = datetime.now(self.timezone)
        self.tomorrow = self.currentTime + timedelta(days=1)
        self.currentWeekday = self.currentTime.weekday()
        self.tomrrowWeekday = self.tomorrow.weekday()

        # Set a flag if the stop times query overflows to next day
        self.nextDayOverflow = False       

        # Create a list with names of the week to help with calendar retrieval
        self.dayOfWeekMap = ['monday', 'tuesday', 'wednesday',
            'thursday', 'friday', 'saturday', 'sunday']

    def getStopTimesAtStop(self, stopId):
        # Query stops times for all trips at this stop
        allTripsAtStop = StopTimes.objects.filter(agency = self.agency, stop_id = stopId)

        if allTripsAtStop:
            # If query succeeded, proceed to...

            # Get timestamp for 60 minutes from now
            limitTstamp = self.currentTime + timedelta(minutes=60)

            if limitTstamp.hour < self.currentTime.hour:
                # Time overflows to the next day

                # Set next day flag to true
                self.nextDayOverflow = True

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

    def calendarCheck(self, tripServiceId, weekNum):
        # Given a trip's service ID determine if it runs on the
        # specified day of the week (either today or tomorrow)

        # Loop through calendar data
        for entry in self.calendarInfo:
            item = entry['fields']

            # Check for matching service ID
            if item['service_id'] == tripServiceId:                
                # Once a matching service ID is found, proceed to...
                
                # Check day of week
                if item[self.dayOfWeekMap[weekNum]] == 1:
                    # Return true if service runs on specified day (indicated by binary 1)
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

        # Loop through all entries in the query response
        for vehicle in response:
            # Get vehicle's trip data
            tripInfo = self.getTripInfo(vehicle['fields']['trip_id'])

            # Get vehicle's arrival time
            arrivalTime = vehicle['fields']['arrival_time'].split(":")
            arrivalHour = int(arrivalTime[0])
            arrivalMinute = int(arrivalTime[1])
            arrivalSecond = int(arrivalTime[2])

            # Create the arrivalDatetime and weekNum fields
            weekNum = None
            arrivalDatetime = None

            # Create the arrival datetime objects past a next day overflow and
            # after-midnight check
            if (self.nextDayOverflow == True and arrivalHour < self.currentTime.hour):
                # Set weekNum to tomorrow's
                weekNum = self.tomrrowWeekday

                # Use month/day/year for tomorrow's date and plug in the arrival time's
                # hour/minute/second to create the arrival datetime
                arrivalDatetime = datetime(
                    self.tomorrow.year,
                    self.tomorrow.month,
                    self.tomorrow.day,
                    arrivalHour,
                    arrivalMinute,
                    arrivalSecond,
                    00000,
                    tzinfo=self.timezone)

            else:
                # Set weekNum to today's
                weekNum = self.currentWeekday

                # Use today's date for the arrival datetime if the time did not overflow
                arrivalDatetime = datetime(
                    self.currentTime.year,
                    self.currentTime.month,
                    self.currentTime.day,
                    arrivalHour,
                    arrivalMinute,
                    arrivalSecond,
                    00000,
                    tzinfo=self.timezone)

            # After getting the arrival datetime,
            # look at calendar data to see if the trip is actually running
            if (self.calendarCheck(tripInfo['service_id'], weekNum) == True):
                # If trip is running, proceed to...

                # Get vehicle's route data
                routeInfo = self.getRouteInfo(tripInfo['route_id'])

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

            # Do nothing and do not add if trip is not running

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
