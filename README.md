# dc-transit-demo

This is a simple API that pulls in data from two different public transit agencies (in thise case the
DC Circulator and DC Metro Rail, with potential for more) and aggregating them in a standardized format.

This is done within the Django framework. To set up create a virtual environment named `env1` and run
`pip install -r requirements.txt` inside it to install all the necessary dependencies.

[views.py](): The views file that handles the parameters typed in and creates the corresponding parser instances
[dcCirculator.py](): Parser class for DC Circulator's Data
[dcMetrorail.py](): Parser class for the DC Metrorail's Data

The response includes the name of the agency (only DC Circulator or DC Metrorail) and the stop name, followed
by the list of buses or trains, each including the following fields: full and abbreviated route names, destination,
direction, minutes away, and vehicle ID, though some may be left null.

I tested this on my local by navigating to `localhost:8000/transit/?` followed by the `circulator` and/or 
`metrorail` paramters with stop IDs.

Example calls:

`localhost:8000/transit/?circulator=12&metrorail=A01`
`localhost:8000/transit/?circulator=8001`
`localhost:8000/transit/?metrorail=B01`

DC Metro's station codes are listed on Wikipedia

Circulator's stop IDs can be found by calling their API for each route like so:
`http://webservices.nextbus.com/service/publicXMLFeed?command=routeConfig&a=dc-circulator&r=yellow`, where
'yellow' can be replaced with the other route tags, which includes 'yellow', 'green', 'blue', 'rosslyn',
'potomac', and 'mall'.
