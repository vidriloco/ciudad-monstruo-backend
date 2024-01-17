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
    source = models.CharField()

    @staticmethod
    def pedestrian_types():
        return {
            'ROBO A TRANSEUNTE EN VIA PUBLICA SIN VIOLENCIA': 'pedestrian-theft',
            'ROBO A TRANSEUNTE EN VIA PUBLICA CON VIOLENCIA': 'pedestrian-theft-violence',
            'HOMICIDIO CULPOSO POR TRÁNSITO VEHICULAR (CAIDA)': 'transit-accident-fall',
            'HOMICIDIO CULPOSO POR TRÁNSITO VEHICULAR (ATROPELLADO)': 'transit-accident-pedestrian',
            'ROBO A PASAJERO / CONDUCTOR DE VEHICULO CON VIOLENCIA': 'passenger-theft-violence',
            'ROBO A PASAJERO A BORDO DE METRO SIN VIOLENCIA': 'metro-theft',
            'ROBO A PASAJERO A BORDO DE METRO CON VIOLENCIA': 'metro-theft-violence',
            'ROBO A PASAJERO A BORDO DE METROBUS SIN VIOLENCIA':  'metrobus-theft',
            'ROBO A PASAJERO A BORDO DE METROBUS CON VIOLENCIA': 'metrobus-theft-violence',
            'ROBO A PASAJERO A BORDO DE PESERO COLECTIVO SIN VIOLENCIA': 'microbus-theft',
            'ROBO A PASAJERO A BORDO DE PESERO COLECTIVO CON VIOLENCIA': 'microbus-theft-violence',
            'ROBO A PASAJERO A BORDO DE TRANSPORTE PÚBLICO SIN VIOLENCIA': 'pt-theft',
            'ROBO A PASAJERO A BORDO DE TRANSPORTE PÚBLICO CON VIOLENCIA': 'pt-theft-violence',
            'ROBO A PASAJERO EN TREN LIGERO SIN VIOLENCIA': 'light-train-theft',
            'ROBO A PASAJERO EN TREN LIGERO CON VIOLENCIA': 'light-train-theft-violence',
            'ROBO A PASAJERO EN TREN SUBURBANO SIN VIOLENCIA': 'suburban-train-theft',
            'ROBO A PASAJERO EN TREN SUBURBANO CON VIOLENCIA': 'suburban-train-theft-violence',
            'ROBO A PASAJERO EN TROLEBUS SIN VIOLENCIA': 'trolebus-theft',
            'ROBO A PASAJERO EN TROLEBUS CON VIOLENCIA': 'trolebus-theft-violence',
            'ROBO A PASAJERO EN RTP SIN VIOLENCIA': 'rtp-bus-theft',
            'ROBO A PASAJERO EN RTP CON VIOLENCIA': 'rtp-bus-theft-violence',
            'ROBO A PASAJERO EN AUTOBUS FORANEO SIN VIOLENCIA': 'foreign-bus-theft',
            'ROBO A PASAJERO EN AUTOBUS FORANEO CON VIOLENCIA': 'foreign-bus-theft-violence',
            'ROBO A PASAJERO EN AUTOBÚS FORÁNEO SIN VIOLENCIA': 'foreign-bus-theft-violence',
            'ROBO A PASAJERO EN AUTOBÚS FORÁNEO CON VIOLENCIA': 'foreign-bus-theft',
            'ROBO A PASAJERO A BORDO DE CABLEBUS SIN VIOLENCIA': 'cablebus-theft',
            'ROBO A PASAJERO A BORDO DE CABLEBUS CON VIOLENCIA': 'cablebus-theft-violence',
            'ROBO A PASAJERO EN ECOBUS SIN VIOLENCIA': 'ecobus-theft',
            'ROBO A PASAJERO EN ECOBUS CON VIOLENCIA': 'ecobus-theft-violence',
            'Atropellado': 'pedestrian-accident'
        }

    @staticmethod
    def cyclist_types():
        return {
            'ROBO DE VEHICULO DE PEDALES': 'bike-theft',
            'Ciclista': 'bike-accident'
        }

    @staticmethod
    def motocyclist_types():
        return {
            'ROBO DE MOTOCICLETA SIN VIOLENCIA': 'motorcicle-theft',
            'ROBO DE MOTOCICLETA CON VIOLENCIA': 'motorcicle-theft-violence',
            'Motociclista': 'motorcicle-accident'
        }
    
    @staticmethod
    def car_driver_types():
        return {
            'HOMICIDIO CULPOSO POR TRÁNSITO VEHICULAR (COLISION)': 'transit-accident-crash',
            'ROBO DE ACCESORIOS DE AUTO': 'car-accessories-theft',
            'ROBO DE VEHICULO DE SERVICIO PARTICULAR CON VIOLENCIA': 'car-theft-violence',
            'ROBO DE VEHICULO DE SERVICIO PARTICULAR SIN VIOLENCIA': 'car-theft',
            'ROBO DE OBJETOS DEL INTERIOR DE UN VEHICULO': 'car-internal-belongings-theft',
            'Choque con lesionados': 'crash-accident',
            'Choque sin lesionados': 'crash-accident',
        }

    @staticmethod
    def types_for_incident_type(incident_type):
        if incident_type == "pedestrian":
            return VictimReport.pedestrian_types()
        elif incident_type == "cyclist":
            return VictimReport.cyclist_types()
        elif incident_type == "motocyclist":
            return VictimReport.motocyclist_types()
        elif incident_type == "car-driver":
            return VictimReport.car_driver_types()
        else:
            return []

    @staticmethod
    def findAllIncidents(ageb_instance, user_profile_type):
        return VictimReport.objects.filter(
            agebvictimreport__ageb_id=ageb_instance.id,
            felony__in=VictimReport.types_for_incident_type(user_profile_type).keys(),
        )
    
    def incident_type(self):
        all_types = {**VictimReport.pedestrian_types(), **VictimReport.cyclist_types(), **VictimReport.motocyclist_types(), **VictimReport.car_driver_types()}
        return all_types[self.felony]

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
            'ROBO A PASAJERO / CONDUCTOR DE VEHICULO CON VIOLENCIA',
            'ROBO A PASAJERO A BORDO DE METRO SIN VIOLENCIA',
            'ROBO A PASAJERO A BORDO DE METRO CON VIOLENCIA',
            'ROBO A PASAJERO A BORDO DE METROBUS SIN VIOLENCIA',
            'ROBO A PASAJERO A BORDO DE METROBUS CON VIOLENCIA',
            'ROBO A PASAJERO A BORDO DE PESERO COLECTIVO SIN VIOLENCIA',
            'ROBO A PASAJERO A BORDO DE PESERO COLECTIVO CON VIOLENCIA',
            'ROBO A PASAJERO A BORDO DE TRANSPORTE PÚBLICO SIN VIOLENCIA',
            'ROBO A PASAJERO A BORDO DE TRANSPORTE PÚBLICO CON VIOLENCIA',
            'ROBO A PASAJERO EN TREN LIGERO SIN VIOLENCIA',
            'ROBO A PASAJERO EN TREN LIGERO CON VIOLENCIA',
            'ROBO A PASAJERO EN TREN SUBURBANO SIN VIOLENCIA',
            'ROBO A PASAJERO EN TREN SUBURBANO CON VIOLENCIA',
            'ROBO A PASAJERO EN TROLEBUS SIN VIOLENCIA',
            'ROBO A PASAJERO EN TROLEBUS CON VIOLENCIA',
            'ROBO A PASAJERO EN RTP SIN VIOLENCIA',
            'ROBO A PASAJERO EN RTP CON VIOLENCIA',
            'ROBO A PASAJERO EN AUTOBUS FORANEO SIN VIOLENCIA',
            'ROBO A PASAJERO EN AUTOBUS FORANEO CON VIOLENCIA',
            'ROBO A PASAJERO EN AUTOBÚS FORÁNEO SIN VIOLENCIA',
            'ROBO A PASAJERO EN AUTOBÚS FORÁNEO CON VIOLENCIA',
            'ROBO A PASAJERO A BORDO DE CABLEBUS SIN VIOLENCIA',
            'ROBO A PASAJERO A BORDO DE CABLEBUS CON VIOLENCIA',
            'ROBO A PASAJERO EN ECOBUS SIN VIOLENCIA',
            'ROBO A PASAJERO EN ECOBUS CON VIOLENCIA'
        }
        
        for victim in victims:
            results[victim.felony].append(victim)
        return results
    
    @staticmethod
    def allCategories():
        return VictimReport.objects.values('felony').annotate(count=models.Count('id'))
    
        