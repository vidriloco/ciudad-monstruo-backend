from django.http import JsonResponse
from world.models import VictimReport

def stolen_bikes(request):
    min_lon = request.GET.get('min_lon')
    min_lat = request.GET.get('min_lat')
    max_lon = request.GET.get('max_lon')
    max_lat = request.GET.get('max_lat')
    
    victims = VictimReport.findAllBikeTheftsWithinViewport(min_lon, min_lat, max_lon, max_lat)
    return JsonResponse({ 'victims': serialize_records(victims) }, status=200)
    
def serialize_records(records):
    return [{'id': record.id, 'location': record.coordinates.coords, 'category': record.felony } for record in records]