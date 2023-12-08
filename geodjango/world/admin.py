from django.contrib import admin
from .models import VictimReport

@admin.register(VictimReport)

class VictimReportAdmin(admin.ModelAdmin):
   list_display=['year', 'date', 'time', 'felony', 'category', 'coordinates', 'reporter_genre', 'reporter_status', 'reporter_type']