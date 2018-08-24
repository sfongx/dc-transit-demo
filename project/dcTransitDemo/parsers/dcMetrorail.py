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
        return ''
    
    def getResponse(self, stopId):
        # First get the raw response by making the request to the API
        rawResponse = self.makeRequest(stopId)

        # Return the parsed response        
        # return self.parseResponse(rawResponse)
        return rawResponse

