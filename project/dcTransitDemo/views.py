from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from .parsers.abstractTransit import AbstractTransit
from .parsers.dcCirculator import DCCirculator
from .parsers.dcMetrorail import DCMetrorail
from .parsers.dcMetrobus import DCMetrobus
from .parsers.gtfsGeneric import GtfsGeneric

from .help.metrorailHelp import metrorailLineSearch, metrorailStopSearch
from .help.metrobusHelp import metrobusStopSearch
from .help.circulatorHelp import circulatorRouteSearch, circulatorStopSearch

import json, logging

def paramCheck(circulator, metrorail, metrobus, vre, mtaMd):
    # Helper function to see if any paramters were provided
    if circulator or metrorail or metrobus or vre or mtaMd:
        return True
    else:
        return False


def handleStandardRequest(request):
    # Project currently supports plugging multiple stop Ids separated by commas per parameter    
    circulatorIds = request.GET.get('circulator', None)
    metrorailIds = request.GET.get('metrorail', None)
    metrobusIds = request.GET.get('metrobus', None)
    mtaMdIds = request.GET.get('mtamd', None)
    vreIds = request.GET.get('vre', None)

    if paramCheck(circulatorIds, metrorailIds, metrobusIds, mtaMdIds, vreIds) == False:
        # If none of the three params are set return an error message
        errorMessage = {
            'error': 'Please provide a stop ID for at least one agency'
        }
        return JsonResponse(errorMessage, safe=False)

    # Pair each stop ID requested with the corresponding parser class
    parserPairs = []
    if circulatorIds:        
        parserPairs.append((DCCirculator(), circulatorIds.split(",")))

    if metrorailIds:        
        parserPairs.append((DCMetrorail(), metrorailIds.split(",")))
    
    if metrobusIds:
        parserPairs.append((DCMetrobus(), metrobusIds.split(",")))

    if mtaMdIds:            
        parserPairs.append((GtfsGeneric("mta-md"), mtaMdIds.split(",")))

    if vreIds:
        parserPairs.append((GtfsGeneric("vre"), vreIds.split(",")))

    # Initialize empty list to return as the response
    responseList = []

    # Loop through and get the response for each
    for parserPair in parserPairs:
        # Specific agency parser is the first value in the tuple
        parser = parserPair[0]

        # List of stop IDs is the second value
        stopIds = parserPair[1]

        # Proceed to loop through stop IDs for this agency
        for stopId in stopIds:
            responseList.append(parser.getResponse(stopId))

    return JsonResponse(responseList, safe=False)

def handleMetrobusStops(request):
    # Latitude, longitude, and radius are required to search for metrobus stops
    lat = request.GET.get('lat', None)
    lon = request.GET.get('lon', None)
    rad = request.GET.get('radius', None)

    if lat and lon and rad:
        # If provided plug them into metrobusStopSearch and return its result
        return JsonResponse(metrobusStopSearch(lat, lon, rad), safe=False)
    else:
        # If at least one of the three are not present return an error message
        errorMessage = {
            'error': 'Please provide a latitude, longitude, and radius'
        }
        return JsonResponse(errorMessage, safe=False)

def handleMetrorailStops(request):
    # Line code is needed to search for metrorail stations
    lineCode = request.GET.get('code', None)

    if lineCode:
        # If provided plug the line code into metrorailStopSearch and return its result
        return JsonResponse(metrorailStopSearch(lineCode), safe=False)
    else:
        # If not provided return an error message
        errorMessage = {
            'error': 'Please provide a line code'
        }
        return JsonResponse(errorMessage, safe=False)

def handleMetrorailLines(request):
    # No params are required for the metroraillines endpoint
    return JsonResponse(metrorailLineSearch(), safe=False)

def handleCirculatorStops(request):
    # NextBus route tag is required to search for circulator stops
    routeTag = request.GET.get('tag', None)

    if routeTag:
        # If provided plug the route tag into circulatorStopSearch and return its result
        return JsonResponse(circulatorStopSearch(routeTag), safe=False)
    else:
        # If not provided return an error message
        errorMessage = {
            'error': 'Please provide a route tag'
        }
        return JsonResponse(errorMessage, safe=False)

def handleCirculatorRoutes(request):
    # No params are required for the circulatorroutes endpoint
    return JsonResponse(circulatorRouteSearch(), safe=False)

