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

        print("Loading transit incidents from C5")
        for idx, row in enumerate(DictReader(open('./inViales-2023.csv'))):
            print("Inserting row number "+ str(idx))
            latitude = 0 if row['latitud'] == "NA" else row['latitud']
            longitude = 0 if row['longitud'] == "NA" else row['longitud']
            report=VictimReport(
                year= 2023,
                date= None if row['fecha_creacion'] == "NA" else row['fecha_creacion'],
                time=row['hora_creacion'],
                felony=row['incidente_c4'],
                category=row['tipo_incidente_c4'],
                reporter_genre="DESCONOCIDO",
                reporter_age= 0,
                reporter_type="FISICA",
                reporter_status=row['clas_con_f_alarma'],
                competence=row['tipo_entrada'],
                coordinates=Point(float(longitude), float(latitude)),
                source="C5")
            report.save()