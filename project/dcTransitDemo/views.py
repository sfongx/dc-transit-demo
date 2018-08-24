from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from .parsers.abstractTransit import AbstractTransit
from .parsers.dcCirculator import DCCirculator
from .parsers.dcMetrorail import DCMetrorail

# Create your views here.
def handleRequest(request):
    circulatorId = request.GET.get('circulator', None)
    metrorailId = request.GET.get('metrorail', None)
    # metrobusId = request.GET.get('metrobus', None)

    parserPairs = []
    if circulatorId:
        parserPairs.append((DCCirculator(), circulatorId))
        
    if metrorailId:
        parserPairs.append((DCMetrorail(), metrorailId))

    # other if checks for metro rail & bus ...

    # Initialize empty list to return as the response
    responseList = []
    for parserPair in parserPairs:
        parser = parserPair[0]
        stopId = parserPair[1]
        responseList.append(parser.getResponse(stopId))

    return JsonResponse(responseList, safe=False)
