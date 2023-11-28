from django.contrib.gis.db import models
from django.contrib.gis.geos import Point, Polygon

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
    coordinates = models.PointField(srid=4326)
    
    @staticmethod
    def findAllWithinViewport(min_longitude, min_latitude, max_longitude, max_latitude):
        bbox_coords = (min_longitude, min_latitude, max_longitude, max_latitude)
        
        bbox = Polygon.from_bbox(bbox_coords)
        
        return VictimReport.objects.filter(coordinates__within=bbox)
    
    @staticmethod
    def findAllBikeTheftsWithinViewport(min_longitude, min_latitude, max_longitude, max_latitude):
        bbox_coords = (min_longitude, min_latitude, max_longitude, max_latitude)
        
        bbox = Polygon.from_bbox(bbox_coords)
        
        return VictimReport.objects.filter(coordinates__within=bbox, felony="ROBO DE VEHICULO DE PEDALES")
    
    @staticmethod
    def allCategories():
        return VictimReport.objects.values('felony').annotate(count=models.Count('id'))
    
        