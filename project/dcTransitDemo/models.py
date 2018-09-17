from django.db import models

# Create your models here.

# GTFS Data. Migrations for new GTFS agency
# MTA Maryland: mta-maryland.
# VRE: vre

# Agency: Name, Slug, GTFS link

class Agency(models.Model):
    name = models.CharField(max_length=31)
    slug = models.SlugField(max_length=31, primary_key=True)
    gtfs_link = models.URLField()

    # Identify all agencies in other classes by their unique slug
    def __str__(self):
        return "%s" % (self.slug)

class Stops(models.Model):
    agency_slug = models.ForeignKey('Agency', on_delete=models.CASCADE)
    agency_stop_id = models.CharField(max_length=63)
    stop_name = models.CharField(max_length=63)
    lat = models.FloatField()
    lon = models.FloatField()

class Routes(models.Model):
    # Text & background colors not required.
    # Some routes.txt files may provide either a short or a long name but not both
    # Will be inserted as a "-" if blank

    agency_slug = models.ForeignKey('Agency', on_delete=models.CASCADE)
    internal_agency_id = models.IntegerField()
    agency_route_id = models.CharField(max_length=31)
    short_name = models.CharField(max_length=31)
    long_name = models.TextField()
    text_color = models.CharField(max_length=6, null=True)
    background_color = models.CharField(max_length=6, null=True)
    
class Trips(models.Model):
    agency_slug = models.ForeignKey('Agency', on_delete=models.CASCADE)
    agency_route_id = models.TextField()
    trip_id = models.TextField()
