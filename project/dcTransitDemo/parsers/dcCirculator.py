from .abstractTransit import AbstractTransit
import http.client, urllib.request, urllib.parse, urllib.error, base64
import xmltodict
import json

class DCCirculator(AbstractTransit):
    def makeRequest(self, stopId):
        # Set up the URL
        url = 'http://webservices.nextbus.com/service/publicXMLFeed?command=predictions&a=dc-circulator&stopId=%d' % int(stopId)

        # Get raw XML Response
        xmlResponse = urllib.request.urlopen(url)

        # Convert XML to dict
        xmlDict = xmltodict.parse(xmlResponse.read().decode('utf-8'))

        return xmlDict

    def parseResponse(self, response):
        return
    
    def getResponse(self, stopId):
        rawResponse = self.makeRequest(stopId)
        
        return rawResponse

