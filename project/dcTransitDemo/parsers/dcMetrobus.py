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

        # Attempt to make the request and get the raw response
        try:
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

        # In the event of an http error catch it
        except urllib.error.HTTPError as err:
            raise Exception("HTTP Error %d" %err.code)
        
    def parseResponse(self, response, stopId):
        # First check for an error message
        if 'Message' in response:
            # If there is an error message assume a bad stop ID was provided
            return {
                'error': 'DC Metrobus stop ID %s is not valid' % stopId
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

        # Point to the API response's 'Predictions' section
        response = response['Predictions']

        # Grab relevant information for each bus
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
        # First attempt get the raw response by making the request to the API
        try:
            rawResponse = self.makeRequest(stopId)
            
            # Return the parsed response        
            return self.parseResponse(rawResponse, stopId)

            # For testing purposes
            # return rawResponse

        # makeRequest will throw an exception if it gets an http error
        except Exception as e:
            return str(e)


