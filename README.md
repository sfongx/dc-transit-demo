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

`localhost:8000/transit/?metrobus=1001319&metrorail=A01&circulator=12`

`localhost:8000/transit/?circulator=8001`

`localhost:8000/transit/?metrobus=1001319`

`localhost:8000/transit/?metrorail=B01`

Example Response:

```[
  {
    "predictions": [
      {
        "destination": null,
        "fullRoute": "Georgetown - Union Station",
        "shortRoute": "yellow",
        "minutes": 7,
        "direction": "Westbound",
        "vehicleId": "2121"
      },
      {
        "destination": null,
        "fullRoute": "Georgetown - Union Station",
        "shortRoute": "yellow",
        "minutes": 27,
        "direction": "Westbound",
        "vehicleId": "2108"
      },
      {
        "destination": null,
        "fullRoute": "Georgetown - Union Station",
        "shortRoute": "yellow",
        "minutes": 57,
        "direction": "Westbound",
        "vehicleId": "3005"
      },
      {
        "destination": null,
        "fullRoute": "Georgetown - Union Station",
        "shortRoute": "yellow",
        "minutes": 67,
        "direction": "Westbound",
        "vehicleId": "2009"
      },
      {
        "destination": null,
        "fullRoute": "Georgetown - Union Station",
        "shortRoute": "yellow",
        "minutes": 77,
        "direction": "Westbound",
        "vehicleId": "2114"
      }
    ],
    "stopName": "K Street NW And 19th Street NW",
    "agencyName": "DC Circulator"
  },
  {
    "predictions": [
      {
        "destination": "Shady Grove",
        "fullRoute": "Red",
        "shortRoute": "RD",
        "minutes": 0,
        "direction": "2",
        "vehicleId": null
      },
      {
        "destination": "Glenmont",
        "fullRoute": "Red",
        "shortRoute": "RD",
        "minutes": 1,
        "direction": "1",
        "vehicleId": null
      },
      {
        "destination": "Silver Spring",
        "fullRoute": "Red",
        "shortRoute": "RD",
        "minutes": 3,
        "direction": "1",
        "vehicleId": null
      },
      {
        "destination": "Glenmont",
        "fullRoute": "Red",
        "shortRoute": "RD",
        "minutes": 4,
        "direction": "1",
        "vehicleId": null
      },
      {
        "destination": "Grosvenor-Strathmore",
        "fullRoute": "Red",
        "shortRoute": "RD",
        "minutes": 1000,
        "direction": "2",
        "vehicleId": null
      },
      {
        "destination": "Shady Grove",
        "fullRoute": "Red",
        "shortRoute": "RD",
        "minutes": 1000,
        "direction": "2",
        "vehicleId": null
      }
    ],
    "stopName": "Metro Center",
    "agencyName": "DC Metrorail"
  },
  {
    "predictions": [
      {
        "destination": "East to Farragut Square",
        "fullRoute": null,
        "shortRoute": "38B",
        "minutes": 0,
        "direction": "0",
        "vehicleId": "3124"
      },
      {
        "destination": "South to Federal Triangle",
        "fullRoute": null,
        "shortRoute": "33",
        "minutes": 6,
        "direction": "1",
        "vehicleId": "7145"
      },
      {
        "destination": "East to Farragut Square",
        "fullRoute": null,
        "shortRoute": "38B",
        "minutes": 6,
        "direction": "0",
        "vehicleId": "2652"
      },
      {
        "destination": "South to Foggy Bottom Station",
        "fullRoute": null,
        "shortRoute": "31",
        "minutes": 8,
        "direction": "1",
        "vehicleId": "7149"
      },
      {
        "destination": "East to Naylor Rd Station",
        "fullRoute": null,
        "shortRoute": "30N",
        "minutes": 15,
        "direction": "0",
        "vehicleId": "6524"
      },
      {
        "destination": "South to Foggy Bottom Station",
        "fullRoute": null,
        "shortRoute": "31",
        "minutes": 21,
        "direction": "1",
        "vehicleId": "7139"
      },
      {
        "destination": "South to Federal Triangle",
        "fullRoute": null,
        "shortRoute": "33",
        "minutes": 41,
        "direction": "1",
        "vehicleId": "6496"
      }
    ],
    "stopName": "M St Nw + Wisconsin Ave Nw",
    "agencyName": "DC Metrobus"
  }
]
```

**Update 9/6/2018**: I have since implemented a stop ID lookup functionality.

**Metrorail**:

[metrorailHelp.py](https://github.com/sfongx/dc-transit-demo/blob/master/project/dcTransitDemo/help/metrorailHelp.py)

Metrorail station code lookup can be done by calling `localhost:8000/transit/metrorailstops/?code=RD`, where the code param is the
line code. Also line codes can be looked up by calling `localhost:8000/transit/metroraillines/`

**Metrobus**:

[metrobusHelp.py](https://github.com/sfongx/dc-transit-demo/blob/master/project/dcTransitDemo/help/metrobusHelp.py)

Metrobus stops can be looked up by entering in a latitude, longitude, and radius, like so:
`localhost:8000/transit/metrobusstops/?lat=38.807270&lon=-77.060023&radius=1000`, which returns all stops in the area up to the
specified radius in meters

**Circulator**:

[circulatorHelp.py](https://github.com/sfongx/dc-transit-demo/blob/master/project/dcTransitDemo/help/circulatorHelp.py)

Circulator stops can be looked up by calling `localhost:8000/transit/circulatorstops/?tag=yellow` where the tag param is the
route tag. Also route tags can be looked up by calling `localhost:8000/transit/circulatorroutes/`

Stop lookups for all three modes will show the actual stop name and coordinates (which help in looking up
metrobus stops) in addition to the stop ID.

Example response for stop lookups:

```[
  {
    "lat": 38.8971951,
    "lon": -77.07153,
    "stopName": "Rosslyn Metro Station",
    "stopId": "0136"
  },
  {
    "lat": 38.9050201,
    "lon": -77.067573,
    "stopName": "34th St and M St NW",
    "stopId": "0137"
  },
  {
    "lat": 38.9050599,
    "lon": -77.0654409,
    "stopName": "Potomac St and M St NW",
    "stopId": "0138"
  },
  {
    "lat": 38.9051199,
    "lon": -77.06234,
    "stopName": "Wisconsin Ave and M St NW",
    "stopId": null
  },
  {
    "lat": 38.9051599,
    "lon": -77.0603853,
    "stopName": "Thomas Jefferson St and M St NW",
    "stopId": "0032"
  },
  {
    "lat": 38.9049514,
    "lon": -77.0572747,
    "stopName": "Penn Ave and 28th St",
    "stopId": "0033"
  },
  {
    "lat": 38.90365,
    "lon": -77.0515929,
    "stopName": "24th and L St",
    "stopId": "0139"
  },
  {
    "lat": 38.9051333,
    "lon": -77.0475276,
    "stopName": "New Hampshire and Mass Ave",
    "stopId": "0140"
  },
  {
    "lat": 38.907402,
    "lon": -77.04348,
    "stopName": "19th St and N St (Dupont Metro)",
    "stopId": "0141"
  },
  {
    "lat": 38.9054288,
    "lon": -77.0474509,
    "stopName": "New Hampshire and M St",
    "stopId": "0143"
  },
  {
    "lat": 38.9053014,
    "lon": -77.0511411,
    "stopName": "24th and M St NW",
    "stopId": "0144"
  },
  {
    "lat": 38.905291,
    "lon": -77.0568095,
    "stopName": "28th and M St NW",
    "stopId": "0145"
  },
  {
    "lat": 38.9052698,
    "lon": -77.0594118,
    "stopName": "30th St and M St NW",
    "stopId": "0146"
  },
  {
    "lat": 38.905253,
    "lon": -77.0616653,
    "stopName": "31st St and M St NW",
    "stopId": "0147"
  },
  {
    "lat": 38.905229,
    "lon": -77.063291,
    "stopName": "Wisconsin Ave and M St NW",
    "stopId": "0148"
  },
  {
    "lat": 38.9051633,
    "lon": -77.0659037,
    "stopName": "33rd St and M St NW",
    "stopId": "0149"
  }
]
```

