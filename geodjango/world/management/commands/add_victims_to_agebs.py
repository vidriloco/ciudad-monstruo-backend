import geojson
from django.core.management import BaseCommand
from django.contrib.gis.geos import Point, Polygon
from csv import DictReader

# Import the model 
from world.models import Ageb
from world.models import VictimReport
from world.models import AgebVictimReport

class Command(BaseCommand):

    def handle(self, *args, **options):

        print("Remove existing ageb victims data")
        AgebVictimReport.objects.all().delete()
        
        agebs = Ageb.objects.all()
        victims = VictimReport.objects.all()

        for index, ageb in enumerate(agebs):
            index_presented = index + 1
            print("Processing ageb " + str(index_presented) + "/" + str(len(agebs)) + " with identifier: " + ageb.cve_geo)
            public_transport_theft_reports = VictimReport.objects.filter(coordinates__within=ageb.geometry, felony__startswith='ROBO A PASAJERO')
            ageb.public_transport_assault_events_count = len(public_transport_theft_reports)

            bike_theft_reports = VictimReport.objects.filter(coordinates__within=ageb.geometry, felony="ROBO DE VEHICULO DE PEDALES")
            ageb.bike_theft_events_count = len(bike_theft_reports)

            car_theft_reports = VictimReport.objects.filter(coordinates__within=ageb.geometry, felony="ROBO DE VEHÍCULO CON Y SIN VIOLENCIA")
            ageb.car_theft_events_count = len(car_theft_reports)

            car_accessories_theft_reports = VictimReport.objects.filter(coordinates__within=ageb.geometry, felony="ROBO DE ACCESORIOS DE AUTO")
            ageb.car_accessories_theft_events_count = len(car_accessories_theft_reports)

            car_internal_belongings_theft_reports = VictimReport.objects.filter(coordinates__within=ageb.geometry, felony="ROBO DE OBJETOS DEL INTERIOR DE UN VEHICULO")
            ageb.car_internal_belongings_theft_events_count = len(car_internal_belongings_theft_reports)

            motorcicle_theft_reports = VictimReport.objects.filter(coordinates__within=ageb.geometry, felony__startswith="ROBO DE MOTOCICLETA")
            ageb.motorcicle_theft_events_count = len(motorcicle_theft_reports)

            pedestrian_theft_reports = VictimReport.objects.filter(coordinates__within=ageb.geometry, felony__startswith="ROBO A TRANSEUNTE EN VIA PUBLICA")
            ageb.pedestrian_theft_events_count = len(pedestrian_theft_reports)
            
            ageb.save()

            for victim_report in victims:
                if ageb.geometry.contains(victim_report.coordinates):
                    ageb_victim_report = AgebVictimReport(ageb=ageb, victim_report=victim_report)
                    ageb_victim_report.save() 