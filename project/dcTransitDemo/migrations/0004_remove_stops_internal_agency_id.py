# Generated by Django 2.0.8 on 2018-09-17 20:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dcTransitDemo', '0003_auto_20180917_0121'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stops',
            name='internal_agency_id',
        ),
    ]