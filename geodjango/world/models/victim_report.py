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
    def findAllBikeTheftsWithinViewport(min_longitude, min_latitude, max_longitude, max_latitude, max_results):
        bbox_coords = (min_longitude, min_latitude, max_longitude, max_latitude)

        bbox = Polygon.from_bbox(bbox_coords)
        
        return VictimReport.objects.filter(coordinates__within=bbox, felony="ROBO DE VEHICULO DE PEDALES")[:int(max_results)]

    @staticmethod
    def findAllTransitIncidentsWithinViewport(min_longitude, min_latitude, max_longitude, max_latitude, max_results):
        bbox_coords = (min_longitude, min_latitude, max_longitude, max_latitude)
        
        bbox = Polygon.from_bbox(bbox_coords)
        
        victims = VictimReport.objects.filter(coordinates__within=bbox, felony__startswith='HOMICIDIO CULPOSO POR TRÁNSITO VEHICULAR').annotate(record_count=Count('id'))[:int(max_results)]
        
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
    def findAllPublicTransportTheftsWithinViewport(min_longitude, min_latitude, max_longitude, max_latitude, max_results):
        bbox_coords = (min_longitude, min_latitude, max_longitude, max_latitude)
        
        bbox = Polygon.from_bbox(bbox_coords)
        
        victims = VictimReport.objects.filter(coordinates__within=bbox, felony__startswith='ROBO A PASAJERO').annotate(record_count=Count('id'))[:int(max_results)]
        
        results = {
            'ROBO A PASAJERO / CONDUCTOR DE VEHICULO CON VIOLENCIA': [],
            'ROBO A PASAJERO A BORDO DE METRO SIN VIOLENCIA': [],
            'ROBO A PASAJERO A BORDO DE METRO CON VIOLENCIA': [],
            'ROBO A PASAJERO A BORDO DE METROBUS SIN VIOLENCIA': [],
            'ROBO A PASAJERO A BORDO DE METROBUS CON VIOLENCIA': [],
            'ROBO A PASAJERO A BORDO DE PESERO COLECTIVO SIN VIOLENCIA': [],
            'ROBO A PASAJERO A BORDO DE PESERO COLECTIVO CON VIOLENCIA': [],
            'ROBO A PASAJERO A BORDO DE TRANSPORTE PÚBLICO SIN VIOLENCIA': [],
            'ROBO A PASAJERO A BORDO DE TRANSPORTE PÚBLICO CON VIOLENCIA': [],
            'ROBO A PASAJERO EN TREN LIGERO SIN VIOLENCIA': [],
            'ROBO A PASAJERO EN TREN LIGERO CON VIOLENCIA': [],
            'ROBO A PASAJERO EN TREN SUBURBANO SIN VIOLENCIA': [],
            'ROBO A PASAJERO EN TREN SUBURBANO CON VIOLENCIA': [],
            'ROBO A PASAJERO EN TROLEBUS SIN VIOLENCIA': [],
            'ROBO A PASAJERO EN TROLEBUS CON VIOLENCIA': [],
            'ROBO A PASAJERO EN RTP SIN VIOLENCIA': [],
            'ROBO A PASAJERO EN RTP CON VIOLENCIA': [],
            'ROBO A PASAJERO EN AUTOBUS FORANEO SIN VIOLENCIA': [],
            'ROBO A PASAJERO EN AUTOBUS FORANEO CON VIOLENCIA': [],
            'ROBO A PASAJERO EN AUTOBÚS FORÁNEO SIN VIOLENCIA': [],
            'ROBO A PASAJERO EN AUTOBÚS FORÁNEO CON VIOLENCIA': [],
            'ROBO A PASAJERO A BORDO DE CABLEBUS SIN VIOLENCIA': [],
            'ROBO A PASAJERO A BORDO DE CABLEBUS CON VIOLENCIA': [],
            'ROBO A PASAJERO EN ECOBUS SIN VIOLENCIA': [],
            'ROBO A PASAJERO EN ECOBUS CON VIOLENCIA': []
        }
        
        for victim in victims:
            results[victim.felony].append(victim)
        return results
    
    @staticmethod
    def allCategories():
        return VictimReport.objects.values('felony').annotate(count=models.Count('id'))
    
        