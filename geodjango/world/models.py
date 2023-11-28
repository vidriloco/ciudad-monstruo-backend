from django.contrib.gis.db import models
from django.contrib.gis.geos import Point, Polygon
from django.db.models import Count

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
    def findAllTransitIncidentsWithinViewport(min_longitude, min_latitude, max_longitude, max_latitude):
        victims = VictimReport.objects.filter(felony__startswith='HOMICIDIO CULPOSO POR TRÁNSITO VEHICULAR').annotate(record_count=Count('id'))
        
        results = {
            'HOMICIDIO CULPOSO POR TRÁNSITO VEHICULAR': [],
            'HOMICIDIO CULPOSO POR TRÁNSITO VEHICULAR (ATROPELLADO)': [],
            'HOMICIDIO CULPOSO POR TRÁNSITO VEHICULAR (CAIDA)': [],
            'HOMICIDIO CULPOSO POR TRÁNSITO VEHICULAR (COLISION)': []
        }
        
        for victim in victims:
            results[victim.felony].append(victim)
        return results
    
    @staticmethod
    def allCategories():
        return VictimReport.objects.values('felony').annotate(count=models.Count('id'))
    
        