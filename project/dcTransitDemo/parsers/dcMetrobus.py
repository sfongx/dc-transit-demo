from .abstractTransit import AbstractTransit
import http.client, urllib.request, urllib.parse, urllib.error, base64
import json

class DCMetrobus(AbstractTransit):

    def makeRequest(self, stopId):
        # Set up the api key
        # IMPORTANT note: this is a key for non-production purposes that can be obtained for free 
        headers = {
            'api_key': '201aad5eaf734234a1e183c5750eaee0',
        }

        # Initialize stop ID as only parameter
        params = urllib.parse.urlencode({
	        'StopID': stopId
        })

        # Make the request
        conn = http.client.HTTPSConnection('api.wmata.com')
        conn.request("GET", "/NextBusService.svc/json/jPredictions?%s" % params, "{body}", headers)

        # Get raw JSON response data
        response = conn.getresponse()
        responseData = response.read().decode("utf-8")
        conn.close()

        # Convert response data to dict
        responseDict = json.loads(responseData)

        return responseDict
        
    def parseResponse(self, response):
        # First check for an error message
        if 'Message' in response:
            # If there is an error message assume a bad stop ID was provided
            return {
                'error': 'DC Metrorail stop ID is not valid'
            }
        
        # Otherwise proceed to grab the following:
        # Stop name, short route name, full route name,
        # direction, destination, minutes away, and vehicle ID

        # Provide data outside of the predictions that includes the stop name and agency
        parsedResponse = {
            'agencyName': 'DC Metrobus',
            'stopName': response['StopName'],
            'predictions': []
        }

        # Now grab the predictions for each bus
        response = response['Predictions']
        for vehicle in response:
            parsedResponse['predictions'].append({
                'shortRoute': vehicle['RouteID'],
                'fullRoute': None,
                'destination': vehicle['DirectionText'],
                'direction': vehicle['DirectionNum'],
                'minutes': int(vehicle['Minutes']),
                'vehicleId': vehicle['VehicleID']
            })

        return parsedResponse

    def getResponse(self, stopId):
        # First get the raw response by making the request to the API
        rawResponse = self.makeRequest(stopId)

        # Return the parsed response        
        return self.parseResponse(rawResponse)

        # For testing purposes
        # return rawResponse
