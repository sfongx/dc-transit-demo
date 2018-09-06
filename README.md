# dc-transit-demo

This is a simple API that pulls in data from two different public transit agencies (in thise case the
DC Circulator and DC Metro Rail, with potential for more) and aggregating them in a standardized format.

This is done within the Django framework. To set up create a virtual environment named `env1` and run
`pip install -r requirements.txt` inside it to install all the necessary dependencies.

[views.py](https://github.com/sfongx/dc-transit-demo/blob/master/project/dcTransitDemo/views.py): The views file that handles the parameters typed in and creates the corresponding parser instances

[dcCirculator.py](https://github.com/sfongx/dc-transit-demo/blob/master/project/dcTransitDemo/parsers/dcCirculator.py): Parser class for 
DC Circulator's Data

[dcMetrorail.py](https://github.com/sfongx/dc-transit-demo/blob/master/project/dcTransitDemo/parsers/dcMetrorail.py): Parser class for 
the DC Metrorail's Data

[abstractTransit.py](https://github.com/sfongx/dc-transit-demo/blob/master/project/dcTransitDemo/parsers/abstractTransit.py): Abstract 
parent parser class that only specifies that the `getResponse` method is required with a provided stop ID.

The response includes the name of the agency (Metrorail, Metrobus, or Circulator) and the stop name, followed
by the list of buses or trains, each including the following fields: full and abbreviated route names, destination,
direction, minutes away, and vehicle ID, though some may be left null.

I tested this on my local by navigating to `localhost:8000/transit/?` followed by the `circulator`, `metrobus`, and/or `metrorail` paramters with stop IDs.

Example calls:

`localhost:8000/transit/?circulator=12&metrorail=A01`

`localhost:8000/transit/?circulator=8001`

`localhost:8000/transit/?metrorail=B01`

Example Response:

```[
  {
    "agencyName": "DC Circulator",
    "predictions": [
      {
        "direction": "Westbound",
        "vehicleId": "2003",
        "destination": null,
        "minutes": 14,
        "shortRoute": "yellow",
        "fullRoute": "Georgetown - Union Station"
      },
      {
        "direction": "Westbound",
        "vehicleId": "1138",
        "destination": null,
        "minutes": 28,
        "shortRoute": "yellow",
        "fullRoute": "Georgetown - Union Station"
      },
      {
        "direction": "Westbound",
        "vehicleId": "1130",
        "destination": null,
        "minutes": 38,
        "shortRoute": "yellow",
        "fullRoute": "Georgetown - Union Station"
      },
      {
        "direction": "Westbound",
        "vehicleId": "2103",
        "destination": null,
        "minutes": 48,
        "shortRoute": "yellow",
        "fullRoute": "Georgetown - Union Station"
      },
      {
        "direction": "Westbound",
        "vehicleId": "2108",
        "destination": null,
        "minutes": 68,
        "shortRoute": "yellow",
        "fullRoute": "Georgetown - Union Station"
      }
    ],
    "stopName": "K Street NW And 19th Street NW"
  },
  {
    "agencyName": "DC Metrorail",
    "predictions": [
      {
        "direction": "1",
        "vehicleId": null,
        "destination": "NoMa-Gallaudet",
        "minutes": 2,
        "shortRoute": "RD",
        "fullRoute": "Red"
      },
      {
        "direction": "1",
        "vehicleId": null,
        "destination": "NoMa-Gallaudet",
        "minutes": 6,
        "shortRoute": "RD",
        "fullRoute": "Red"
      },
      {
        "direction": "2",
        "vehicleId": null,
        "destination": "Shady Grove",
        "minutes": 6,
        "shortRoute": "RD",
        "fullRoute": "Red"
      },
      {
        "direction": "1",
        "vehicleId": null,
        "destination": "NoMa-Gallaudet",
        "minutes": 15,
        "shortRoute": "RD",
        "fullRoute": "Red"
      },
      {
        "direction": "2",
        "vehicleId": null,
        "destination": "Shady Grove",
        "minutes": 15,
        "shortRoute": "RD",
        "fullRoute": "Red"
      },
      {
        "direction": "2",
        "vehicleId": null,
        "destination": "Shady Grove",
        "minutes": 21,
        "shortRoute": "RD",
        "fullRoute": "Red"
      }
    ],
    "stopName": "Metro Center"
  }
]
```

**Update 9/6/2018**: I have since implemented help functionality to look up stop IDs.

**Metrorail**:

[metrorailHelp.py](https://github.com/sfongx/dc-transit-demo/blob/master/project/dcTransitDemo/help/metrorailHelp.py)

Metrorail station code lookup can be done by calling `localhost:8000/transit/metrorailstops/?code=RD`, where the code param is the
line code. Also line codes can be looked up by calling `localhost:8000/transit/metroraillines/`

**Metrobus**:

[metrobusHelp.py](https://github.com/sfongx/dc-transit-demo/blob/master/project/dcTransitDemo/help/metrobusHelp.py)

Metrobus stops can be looked up by entering in a latitude, longitude, and radius, like so:
`http://localhost:8000/transit/metrobusstops/?lat=38.807270&lon=-77.060023&radius=1000`, which returns all stops in the area up to the
specified radius in meters

**Circulator**:

[circulatorHelp.py](https://github.com/sfongx/dc-transit-demo/blob/master/project/dcTransitDemo/help/circulatorHelp.py)

Circulator stops can be looked up by calling `http://localhost:8000/transit/circulatorstops/?tag=yellow` where the tag param is the
route tag. Also route tags can be looked up by calling `localhost:8000/transit/circulatorroutes/`
