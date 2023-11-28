from django.http import HttpResponse
import csv
from world.models import VictimReport

def categories(request):
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="somefilename.csv"'}
    )
    
    writer = csv.writer(response)
    writer.writerow(["Felony types", "Total"])
    categories = VictimReport.allCategories()
    
    for c in categories:
        writer.writerow([c["felony"], c["count"]])
        
    
    return response