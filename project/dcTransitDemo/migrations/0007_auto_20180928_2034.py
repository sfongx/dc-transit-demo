# Generated by Django 2.0.8 on 2018-09-28 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dcTransitDemo', '0006_updateVreData2'),
    ]

    operations = [
        migrations.AddField(
            model_name='trips',
            name='direction',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='trips',
            name='trip_headsign',
            field=models.TextField(null=True),
        ),
    ]