from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from .parsers.abstractTransit import AbstractTransit
from .parsers.dcCirculator import DCCirculator
from .parsers.dcMetrorail import DCMetrorail

# handleRequest only method as part of views
# Look at the provided parameters and create the corresponding parser objects
def handleRequest(request):
    circulatorId = request.GET.get('circulator', None)
    metrorailId = request.GET.get('metrorail', None)

    parserPairs = []
    if circulatorId:
        parserPairs.append((DCCirculator(), circulatorId))

    if metrorailId:
        parserPairs.append((DCMetrorail(), metrorailId))

    # Initialize empty list to return as the response
    responseList = []

    # Loop through and get the response for each
    for parserPair in parserPairs:
        parser = parserPair[0]
        stopId = parserPair[1]
        responseList.append(parser.getResponse(stopId))

    return JsonResponse(responseList, safe=False)
