from csv import DictReader
from django.core.management import BaseCommand
from django.contrib.gis.geos import Point

# Import the model 
from world.models import VictimReport

ALREDY_LOADED_ERROR_MESSAGE = """
If you need to reload the child data from the CSV file,
first delete the db.sqlite3 file to destroy the database.
Then, run `python manage.py migrate` for a new empty
database with tables"""


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from victims.csv"

    def handle(self, *args, **options):
    
        # Show this if the data already exist in the database
        if VictimReport.objects.exists():
            print('victims data already loaded...exiting.')
            print(ALREDY_LOADED_ERROR_MESSAGE)
            return
            
        # Show this before loading the data into the database
        print("Loading victims data")

        #Code to load the data into database
        for row in DictReader(open('./victims-2023.csv')):
            latitude = 0 if row['latitud'] == "NA" else row['latitud']
            longitude = 0 if row['longitud'] == "NA" else row['longitud']
            report=VictimReport(
                year= 0 if row['anio_hecho'] == "NA" else row['anio_hecho'],
                date= None if row['fecha_hecho'] == "NA" else row['fecha_hecho'],
                time=row['hora_hecho'],
                felony=row['delito'],
                category=row['categoria'],
                reporter_genre=row['sexo'],
                reporter_age= 0 if row['edad'] == "NA" else row['edad'],
                reporter_type=row['tipo_persona'],
                reporter_status=row['calidad_juridica'],
                competence=row['competencia'],
                coordinates=Point(float(longitude), float(latitude)))
            report.save()
