from django.contrib import admin
from .models import VictimReport
from .models import Ageb
from .models import AgebVictimReport

@admin.register(VictimReport)

class VictimReportAdmin(admin.ModelAdmin):
   list_display=['year', 'date', 'time', 'felony', 'category', 'coordinates', 'reporter_genre', 'reporter_status', 'reporter_type']

@admin.register(Ageb)

class AgebAdmin(admin.ModelAdmin):
   list_display=['cve_ageb', 'geometry', 'cve_geo', 'public_transport_assault_events_count', 'bike_theft_events_count', 'car_theft_events_count', 'car_accessories_theft_events_count', 'car_internal_belongings_theft_events_count', 'motorcicle_theft_events_count', 'pedestrian_theft_events_count', 'pedestrian_accidents_events_count', 'crash_accidents_events_count', 'motorcicle_accidents_events_count', 'bicicle_accidents_events_count']

@admin.register(AgebVictimReport)

class AgebVictimReportAdmin(admin.ModelAdmin):
   list_display=['ageb', 'victim_report', 'first_category', 'second_category']