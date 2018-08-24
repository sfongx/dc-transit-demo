from .abstractTransit import AbstractTransit
import http.client, urllib.request, urllib.parse, urllib.error, base64
import xmltodict
import json

class DCCirculator(AbstractTransit):
    def makeRequest(self, stopId):
        # Set up the URL
        url = 'http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=dc-circulator&stopId=%s' % stopId

        # Get raw XML Response
        xmlResponse = urllib.request.urlopen(url)

        # Convert XML to dict
        xmlDict = xmltodict.parse(xmlResponse.read().decode('utf-8'))

        return xmlDict

    def parseResponse(self, response):
        # First check to see if a valid stop ID was provided
        response = response['body']
        if 'Error' in response:
            # If not return an error message
            return {
                'error': 'DC Circulator stop ID is not valid'
            }
        
        # Otherwise proceed to grab the following:
        # stop Name, short route name, full route name,
        # direction, destination, and minutes away
        response = response['predictions']
        parsedResponse = {
            'agencyName': 'DC Circulator',
            'stopName': response['@stopTitle'],
            'predictions': []
        }

        # Route name and direction are all the same for each stop ID
        # Using the provided route title as the destination
        # Full route will be tag + route name
        shortRoute = response['@routeTag']
        destination = response['@routeTitle']
        fullRoute = "(" + shortRoute + ") " + destination
        direction = response['direction']['@title']

        # Look at every vehicle individually
        predictions = response['direction']['prediction']

        for vehicle in predictions:
            parsedResponse['predictions'].append({
                'shortRoute': shortRoute,
                'fullRoute': fullRoute,
                'destination': destination,
                'direction': direction,
                'minutes': vehicle['@minutes'],
                'vehicleId': vehicle['@vehicle']
            })

        return parsedResponse
    
    def getResponse(self, stopId):
        # First get the raw response by making the request to the API
        rawResponse = self.makeRequest(stopId)
        
        # Return the parsed response        
        return self.parseResponse(rawResponse)
        # return rawResponse

