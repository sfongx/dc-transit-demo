from django.db import models


# Agency: store data about a GTFS transit agency, including its plain text name,
# GTFS zip link, time zone, last time its data was updated, and unique slug name
class Agency(models.Model):
    name = models.CharField(max_length=31)
    slug = models.SlugField(max_length=31, primary_key=True)
    time_zone = models.CharField(max_length=31)
    last_update = models.TimeField()
    gtfs_link = models.URLField()

    # Identify all agencies in other classes by their slug
    def __str__(self):
        return "%s" % (self.slug)

# Stops: store data about an agency's stops, identified by the agency slug name.
# Includes the stop ID, stop name, and coordinates
class Stops(models.Model):
    agency_slug = models.ForeignKey('Agency', on_delete=models.CASCADE)
    stop_id = models.CharField(max_length=63)
    stop_name = models.CharField(max_length=63)
    lat = models.FloatField()
    lon = models.FloatField()

# Routes: store data about an agency's routes, identified by the agency slug name
# and internal agency ID (some GTFS links include multiple sub-agencies as listed under agency.txt).
# Includes the route ID, either or both the short and long names, and optional
# text and background color. If either the short or long names are not available
# a dash will be put in its place.
class Routes(models.Model):
    agency_slug = models.ForeignKey('Agency', on_delete=models.CASCADE)
    internal_agency_id = models.IntegerField()
    route_id = models.CharField(max_length=31)
    short_name = models.CharField(max_length=31)
    long_name = models.TextField()
    text_color = models.CharField(max_length=6, null=True)
    background_color = models.CharField(max_length=6, null=True)

# Trips: store data about an agency's trips for each route, identified by the agency slug name.
# Includes the corresponding route and trip IDs.
class Trips(models.Model):
    agency_slug = models.ForeignKey('Agency', on_delete=models.CASCADE)
    route_id = models.TextField()
    trip_id = models.TextField()

# StopTimes: store data about the scheduled times for each stop for an agency,
# identified by the agency slug name. Includes the arrival and departure times in hh:mm:ss,
# trip ID, and stop ID.
class StopTimes(models.Model):
    agency_slug = models.ForeignKey('Agency', on_delete=models.CASCADE)
    trip_id = models.TextField()
    stop_id = models.CharField(max_length=63)
    arrival_time = models.TimeField()
    departure_time = models.TimeField()

