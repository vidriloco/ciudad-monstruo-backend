import geojson
from django.core.management import BaseCommand
from django.contrib.gis.geos import Point, Polygon
from csv import DictReader

# Import the model 
from world.models import Ageb
from world.models import VictimReport
from world.models import AgebVictimReport

class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from victims.csv"

    def handle(self, *args, **options):
        
        # Show this if the data already exist in the database
        for ageb in Ageb.objects.all():
            print(AgebVictimReport.objects.filter(ageb=ageb).count())