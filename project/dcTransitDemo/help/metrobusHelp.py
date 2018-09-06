import http.client, urllib.request, urllib.parse, urllib.error, base64
import json

def makeRequest(lat, lon, rad):
    # Set up the api key
    # IMPORTANT note: this is a key for non-production purposes that can be obtained for free 
    headers = {
	    'api_key': '201aad5eaf734234a1e183c5750eaee0',
    }

    # Set up the provided latitidue, longitude, and radius as parameters
    params = urllib.parse.urlencode({
        'Lat': lat,
        'Lon': lon,
        'Radius': rad
    })

    # Attempt to make the request and get the raw response
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

def parseResponse(response):
    # List of stops stored under 'Stops'
    stopList = response['Stops']
    # Initialize empty parsed stop list
    parsedStops = []

    # Grab each stop's relevant information
    for stop in stopList:
        parsedStops.append({
            'stopName': stop['Name'],
            'stopId': stop['StopID'],
            'lat': stop['Lat'],
            'lon': stop['Lon']
        })
    return parsedStops

def metrobusStopSearch(lat, lon, rad):
    # Attempt to make API call to obtain stop IDs given coordinates & radius
    try:
        rawResponse = makeRequest(lat, lon, rad)

        # Parse the response so only the stop ID, name, and coordinates are returned
        return parseResponse(rawResponse)

        # For testing purposes
        # return rawResponse

    except Exception as e:
        return str(e)
