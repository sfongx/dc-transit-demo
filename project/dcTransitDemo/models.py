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

class Stops(models.Model):
    agency_slug = models.SlugField(max_length=31)
    internal_agency_id = models.IntegerField()
    agency_stop_id = models.CharField(max_length=63)
    stop_name = models.CharField(max_length=63)
    lat = models.FloatField()
    lon = models.FloatField()

class Routes(models.Model):
    agency_slug = models.SlugField(max_length=31)
    internal_agency_id = models.IntegerField()
    agency_route_id = models.CharField(max_length=31)
    short_name = models.CharField(max_length=31)
    long_name = models.TextField()
    text_color = models.CharField(max_length=6)
    background_color = models.CharField(max_length=6)
    
class Trips(models.Model):
    agency_slug = models.SlugField(max_length=31)
    agency_route_id = models.TextField()
    trip_id = models.TextField()
