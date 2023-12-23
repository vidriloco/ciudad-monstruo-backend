from django.contrib import admin
from .models import VictimReport
from .models import Ageb

@admin.register(VictimReport)

class VictimReportAdmin(admin.ModelAdmin):
   list_display=['year', 'date', 'time', 'felony', 'category', 'coordinates', 'reporter_genre', 'reporter_status', 'reporter_type']

@admin.register(Ageb)

class AgebAdmin(admin.ModelAdmin):
   list_display=['cve_ageb', 'geometry', 'cve_geo']