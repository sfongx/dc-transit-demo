# Generated by Django 2.0.8 on 2018-09-13 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dcTransitDemo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stops',
            name='agency_stop_id',
            field=models.CharField(max_length=63),
        ),
    ]