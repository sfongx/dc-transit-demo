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
        # First check for an error message
        response = response['body']
        if 'Error' in response:
            # If there is an error message assume  a bad stop ID was provided
            return {
                'error': 'DC Circulator stop ID is not valid'
            }
        
        # Otherwise proceed to grab the following:
        # Stop name, short route name, full route name,
        # direction, destination, minutes away, and vehicle ID

        # Make the response now point to the API response's 'predictions' section
        response = response['predictions']

        # Provide data outside of the predictions that includes the stop name and agency
        parsedResponse = {
            'agencyName': 'DC Circulator',
            'stopName': response['@stopTitle'],
            'predictions': []
        }

        # Route name and direction are all the same for each stop ID
        # Destination will be left blank for all
        shortRoute = response['@routeTag']
        fullRoute = response['@routeTitle']
        direction = response['direction']['@title']

        # Look at every vehicle individually
        predictions = response['direction']['prediction']
        for vehicle in predictions:
            parsedResponse['predictions'].append({
                'shortRoute': shortRoute,
                'fullRoute': fullRoute,
                'destination': None,
                'direction': direction,
                'minutes': int(vehicle['@minutes']),
                'vehicleId': vehicle['@vehicle']
            })

        return parsedResponse
    
    def getResponse(self, stopId):
        # First get the raw response by making the request to the API
        rawResponse = self.makeRequest(stopId)
        
        # Return the parsed response        
        return self.parseResponse(rawResponse)

        # For testing purposes
        # return rawResponse

