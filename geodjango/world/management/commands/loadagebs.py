import geojson
from django.core.management import BaseCommand
from django.contrib.gis.geos import Point, Polygon

# Import the model 
from world.models import Ageb

class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from agebs.json"

    def handle(self, *args, **options):
    
        # Show this if the data already exist in the database
        if Ageb.objects.exists():
            print('Ageb data already loaded...exiting.')
            return
            
        # Show this before loading the data into the database
        print("Ingesting AGEB data")

        #Code to load the data into database
        with open('./agebs.json') as f:
            gj = geojson.load(f)
            features = gj['features']
            for feature in features:
                cve_geo = feature['properties']['CVEGEO']
                cve_ent = feature['properties']['CVE_ENT']
                cve_mun = feature['properties']['CVE_MUN']
                cve_loc = feature['properties']['CVE_LOC']
                cve_ageb = feature['properties']['CVE_AGEB']
                coordinates = feature['geometry']['coordinates'][0]

                points = []
                for coordinate in coordinates:
                    points.append(Point(coordinate[0], coordinate[1]))
                
                ageb = Ageb(cve_geo=cve_geo, cve_ent=cve_ent, cve_mun=cve_mun, cve_loc=cve_loc, cve_ageb=cve_ageb, geometry=Polygon(points))
                ageb.save()
            