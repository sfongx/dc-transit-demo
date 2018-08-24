from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from .parsers.abstractTransit import AbstractTransit
from .parsers.dcCirculator import DCCirculator

# Create your views here.
def handleRequest(request):
    circulatorId = request.GET.get('circulator', None)
    # metrorailId = request.GET.get('metrorail', None)
    # metrobusId = request.GET.get('metrobus', None)

    parserList = []
    if circulatorId:
        c = DCCirculator()
        parserList.append(c)

    # other if checks for metro rail & bus ...

    # Initialize empty list to return as the response
    responseList = []
    for parser in parserList:
        responseList.append(parser.getResponse())

    return JsonResponse(responseList)
