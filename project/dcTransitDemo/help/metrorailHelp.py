import http.client, urllib.request, urllib.parse, urllib.error, base64
import json

def makeRequest(url):
    # Set up the api key
    # IMPORTANT note: this is a key for non-production purposes that can be obtained for free 
    headers = {
	    'api_key': '201aad5eaf734234a1e183c5750eaee0',
    }

    # Attempt to make the request and get the raw response
    try:
        # Make the request
        conn = http.client.HTTPSConnection('api.wmata.com')
        conn.request("GET", url, "{body}", headers)

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

def parseLines(linesResponse):
    # List of lines stored under 'Lines'
    lineList = linesResponse['Lines']

    # Initialize empty parsed line list
    parsedLines = []

    # Grab each line's relevant information
    for line in lineList:
        parsedLines.append({
            'fullName': line['DisplayName'],
            'lineCode': line['LineCode']
        })

    return parsedLines

def parseStops(stopsResponse):
    # List of stations stored under 'Stations'
    stationList = stopsResponse['Stations']

    # Initialize empty parsed stop list
    parsedStops = []

    # Grab each stop's relevant information
    for stop in stationList:
        parsedStops.append({
            'stopName': stop['Name'],
            'stopId': stop['Code'],
            'lat': stop['Lat'],
            'lon': stop['Lon']
        })

    return parsedStops

def metrorailStopSearch(lineCode):
    # Attempt to make API call to obtain stations given a WMATA line code
    try:
        # Set up line code param
        params = urllib.parse.urlencode({
            'LineCode': lineCode
        })

        # Set up URL with the line code param and pass it into makeRequest
        url = "/Rail.svc/json/jStations?%s" % params
        rawResponse = makeRequest(url)

        # Parse the response so only the stop ID, name, and coordinates are returned
        return parseStops(rawResponse)

        # For testing purposes
        # return rawResponse

    except Exception as e:
        return str(e)

def metrorailLineSearch():
    # Attempt to make API call to obtain metro lines and their codes
    try:
        # Set up a blank param
        params = urllib.parse.urlencode({})

        # Set up the url with the blank param and pass it into makeRequest
        url = "/Rail.svc/json/jLines?%s" % params
        rawResponse = makeRequest(url)

        # Parse the response so only the line name and code are returned
        return parseLines(rawResponse)

        # For testing purposes
        # return rawResponse
    
    except Exception as e:
        return str(e)

