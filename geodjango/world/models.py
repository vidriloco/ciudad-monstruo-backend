from django.contrib.gis.db import models

class VictimReport(models.Model):
    year = models.IntegerField()
    date = models.DateField(default=None, blank=True, null=True)
    time = models.CharField()
    felony = models.CharField()
    category = models.CharField()
    reporter_genre = models.CharField()
    reporter_age = models.IntegerField()
    reporter_type = models.CharField()
    reporter_status = models.CharField()
    competence = models.CharField()
    coordinates = models.PointField()