from django.contrib.gis.db import models
from django.contrib.gis.geos import Polygon
from django.db.models import Count

class Ageb(models.Model):
    cve_geo = models.CharField()
    cve_ent = models.IntegerField()
    cve_mun = models.IntegerField()
    cve_loc = models.IntegerField()
    cve_ageb = models.CharField()
    geometry = models.PolygonField(srid=4326)
    public_transport_assault_events_count = models.IntegerField(default=0)
    bike_theft_events_count = models.IntegerField(default=0)
    car_theft_events_count = models.IntegerField(default=0)
    motorcicle_theft_events_count = models.IntegerField(default=0)
    pedestrian_theft_events_count = models.IntegerField(default=0)
    pedestrian_accidents_events_count = models.IntegerField(default=0)
    crash_accidents_events_count = models.IntegerField(default=0)
    motorcicle_accidents_events_count = models.IntegerField(default=0)
    bicicle_accidents_events_count = models.IntegerField(default=0)


class AgebVictimReport(models.Model):
    ageb = models.ForeignKey(Ageb, on_delete=models.CASCADE)
    victim_report = models.ForeignKey('VictimReport', on_delete=models.CASCADE)
    first_category = models.CharField()
    second_category = models.CharField()
