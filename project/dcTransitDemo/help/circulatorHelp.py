import http.client, urllib.request, urllib.parse, urllib.error, base64
import xmltodict
import json

def makeRequest(url):
    # Attempt to make the request. URL already assumed to be set up and passed in
    try:
        # Get raw XML Response
        xmlResponse = urllib.request.urlopen(url)

        # Convert XML to dict
        xmlDict = xmltodict.parse(xmlResponse.read().decode('utf-8'))

        return xmlDict
    
    # In the event of an http error catch it
    except urllib.error.HTTPError as err:
        raise Exception("HTTP Error %d" %err.code)

def parseRoutes(routesResponse):
    # List of routes stored within the 'route' field within 'body'
    routeList = routesResponse['body']['route']

    # Initialize empty parsed route list
    parsedRoutes = []

    # Now grab each route's information
    for route in routeList:
        parsedRoutes.append({
            'tag': route['@tag'],
            'fullRoute': route['@title']
        })

    return parsedRoutes

def parseStops(stopsResponse):
    # List of stops stored under 'body' > 'route' > 'stop'
    stopList = stopsResponse['body']['route']['stop']

    # Initialize empty parsed stop list
    parsedStops = []

    # Grab each stop's relevant information
    for stop in stopList:
        # Some stop IDs are unfortunately not provided
        if '@stopId' in stop:
            # Grab stop ID if present
            stopId = stop['@stopId']
        else:
            # Put in a null value if not
            stopId = None

        # Now put it all together
        parsedStops.append({
            'stopName': stop['@title'],
            'stopId': stopId,
            'lat': float(stop['@lat']),
            'lon': float(stop['@lon'])
        })
    return parsedStops

def circulatorStopSearch(routeTag):
    # Attempt to make API call to obtain stop IDs given the route tag
    try:
        # Set up URL first before passing it to makeRequest
        url = 'http://webservices.nextbus.com/service/publicXMLFeed?command=routeConfig&a=dc-circulator&r=%s' % routeTag
        rawResponse = makeRequest(url)

        # Parse the response so only the name and ID are returned
        return parseStops(rawResponse)

        # For testing purposes
        # return rawResponse

    except Exception as e:
        return str(e)

def circulatorRouteSearch():
    # Attempt to make API call to obtain route tags used by NextBus
    try:
        # Set up URL first before passing it to makeRequest
        url = 'http://webservices.nextbus.com/service/publicXMLFeed?command=routeList&a=dc-circulator'
        rawResponse = makeRequest(url)

        # Parse the response so only the name and ID are returned
        return parseRoutes(rawResponse)

        # For testing purposes
        # return rawResponse

    except Exception as e:
        return str(e)

