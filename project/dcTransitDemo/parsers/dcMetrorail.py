from .abstractTransit import AbstractTransit
import http.client, urllib.request, urllib.parse, urllib.error, base64
import json

class DCMetrorail(AbstractTransit):
    def makeRequest(self, stopId):
        # Set up the api key
        # IMPORTANT note: this is a key for non-production purposes that can be obtained for free 
        headers = {
            'api_key': '201aad5eaf734234a1e183c5750eaee0',
        }

        # Initialize parameters as empty
        params = urllib.parse.urlencode({})

        # Make the request
        conn = http.client.HTTPSConnection('api.wmata.com')
        conn.request("GET", "/StationPrediction.svc/json/GetPrediction/%s?%s" % (stopId, params), "{body}", headers)
        
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

        # Set up a way to map line initials with full color names
        fullNames = {
            'RD': 'Red',
            'GR': 'Green',
            'YL': 'Yellow',
            'BL': 'Blue',
            'OR': 'Orange',
            'SV': 'Silver',
        }

        # Provide data outside of the predictions that includes the stop name and agency
        # The actual stop name is listed with each individual train
        # If no trains are running it cannot be grabbed
        response = response['Trains']
        parsedResponse = {
            'agencyName': 'DC Metrorail',
            'stopName': None,
            'predictions': []
        }

        # Flag for setting the stop name
        stopNameGrabbed = False

        for train in response:
            # If trains are running grab the stop name once
            if stopNameGrabbed == False:
                parsedResponse['stopName'] = train['LocationName']
                stopNameGrabbed = True

            # Process minutes and deal with 'ARR', 'BRD', and 'DLY'
            minutes = train['Min']
            if minutes == 'ARR' or minutes == 'BRD':
                # ARR and BRD will be treated as 0 minutes
                minutes = 0
            elif minutes == 'DLY' or minutes == '':
                # DLY or no value will be arbitrarily treated as '1000' minutes
                minutes = 1000
            else:
                # Normal minute values will be converted as is
                minutes = int(minutes)

            # Now put it together. Vehicle ID will be left blank for all
            parsedResponse['predictions'].append({
                'shortRoute': train['Line'],
                'fullRoute': fullNames[train['Line']],
                'destination': train['DestinationName'],
                'direction': train['Group'],
                'minutes': minutes,
                'vehicleId': None
            })

        return parsedResponse
    
    def getResponse(self, stopId):
        # First get the raw response by making the request to the API
        rawResponse = self.makeRequest(stopId)

        # Return the parsed response        
        return self.parseResponse(rawResponse)

        # For testing purposes
        # return rawResponse

