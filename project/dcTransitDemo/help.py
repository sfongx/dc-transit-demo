import http.client, urllib.request, urllib.parse, urllib.error, base64
import json

def metrobusHelp(lat, lon):
    # Set up the api key
    # IMPORTANT note: this is a key for non-production purposes that can be obtained for free 
    headers = {
	    'api_key': '201aad5eaf734234a1e183c5750eaee0',
    }

    # Set up the provided latitidue and longitude, and radius of '100' as parameters
    params = urllib.parse.urlencode({
        # Request parameters
        'Lat': lat,
        'Lon': lon,
        'Radius': '100',
    })

    # Attempt to make the request
    try:
        # Make the request
        conn = http.client.HTTPSConnection('api.wmata.com')
        conn.request("GET", "/Bus.svc/json/jStops?%s" % params, "{body}", headers)

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
