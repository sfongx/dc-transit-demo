# Generated by Django 2.0.8 on 2018-10-19 00:23

from django.db import migrations

def add_agencies(apps, schema_editor):
    # Only adding MTA Maryland and Virginia Railway Express for now
    Agency = apps.get_model('dcTransitDemo', 'Agency')

    Agency(
        name = 'MTA Maryland',
        slug = 'mta-md',
        time_zone = 'America/New_York',
        last_update = None,
        gtfs_link = 'https://mta.maryland.gov/_googletransit/latest/google_transit.zip'
        ).save()

    Agency(
        name='Virginia Railway Express',
        slug='vre',
        time_zone='America/New_York',
        last_update = None,
        gtfs_link='http://www.vre.org/gtfs/google_transit.zip'
        ).save()

class Migration(migrations.Migration):

    dependencies = [
        ('dcTransitDemo', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_agencies)
    ]
