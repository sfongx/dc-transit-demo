from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from .parsers.abstractTransit import AbstractTransit
from .parsers.dcCirculator import DCCirculator
from .parsers.dcMetrorail import DCMetrorail
from .parsers.dcMetrobus import DCMetrobus

# Look at the provided stop ID paramters and pair them with the corresponding parser objects
def handleRequest(request):
    circulatorId = request.GET.get('circulator', None)
    metrorailId = request.GET.get('metrorail', None)
    metrobusId = request.GET.get('metrobus', None)

    parserPairs = []
    if circulatorId:
        parserPairs.append((DCCirculator(), circulatorId))

    if metrorailId:
        parserPairs.append((DCMetrorail(), metrorailId))
    
    if metrobusId:
        parserPairs.append((DCMetrobus(), metrobusId))

    # Initialize empty list to return as the response
    responseList = []

    # Loop through and get the response for each
    for parserPair in parserPairs:
        parser = parserPair[0]
        stopId = parserPair[1]
        responseList.append(parser.getResponse(stopId))

    return JsonResponse(responseList, safe=False)
