from django.http import JsonResponse
from world.models import VictimReport
from world.models import Ageb
from django.contrib.gis.db.models.functions import Centroid

def agebs(request):
    min_lon = request.GET.get('min_lon')
    min_lat = request.GET.get('min_lat')
    max_lon = request.GET.get('max_lon')
    max_lat = request.GET.get('max_lat')
    max_results = request.GET.get('max_results')
    
    agebs = Ageb.findAllAgebsWithinViewport(min_lon, min_lat, max_lon, max_lat)
    return JsonResponse({ 'agebs': serialize_ageb_records(agebs) }, status=200)

def ageb_details(request, ageb_id):
    category_type = request.GET.get('category_type')
    ageb_instance = Ageb.objects.get(id=ageb_id)
    matching_reports = VictimReport.findAllIncidents(ageb_instance, category_type)

    return JsonResponse({ 'ageb-detail': serialize_ageb_detail_records(ageb_instance, matching_reports) }, status=200)

def stolen_bikes(request):
    min_lon = request.GET.get('min_lon')
    min_lat = request.GET.get('min_lat')
    max_lon = request.GET.get('max_lon')
    max_lat = request.GET.get('max_lat')
    max_results = request.GET.get('max_results')
    
    victims = VictimReport.findAllBikeTheftsWithinViewport(min_lon, min_lat, max_lon, max_lat, max_results)
    return JsonResponse({ 'victims': serialize_records(victims) }, status=200)

def transit_incidents(request):
    min_lon = request.GET.get('min_lon')
    min_lat = request.GET.get('min_lat')
    max_lon = request.GET.get('max_lon')
    max_lat = request.GET.get('max_lat')
    max_results = request.GET.get('max_results')
    
    victims = VictimReport.findAllTransitIncidentsWithinViewport(min_lon, min_lat, max_lon, max_lat, max_results)
    
    return JsonResponse({ 'victims': {
        'transit-accident': serialize_records(victims['HOMICIDIO CULPOSO POR TRÁNSITO VEHICULAR']),
        'transit-accident-pedestrian': serialize_records(victims['HOMICIDIO CULPOSO POR TRÁNSITO VEHICULAR (ATROPELLADO)']),
        'transit-accident-fall': serialize_records(victims['HOMICIDIO CULPOSO POR TRÁNSITO VEHICULAR (CAIDA)']),
        'transit-accident-crash': serialize_records(victims['HOMICIDIO CULPOSO POR TRÁNSITO VEHICULAR (COLISION)'])
    } }, status=200)

def public_transport_incidents(request):
    min_lon = request.GET.get('min_lon')
    min_lat = request.GET.get('min_lat')
    max_lon = request.GET.get('max_lon')
    max_lat = request.GET.get('max_lat')
    max_results = request.GET.get('max_results')
    
    victims = VictimReport.findAllPublicTransportTheftsWithinViewport(min_lon, min_lat, max_lon, max_lat, max_results)
    
    return JsonResponse({ 'victims': {
        'metro-theft': serialize_records(victims['ROBO A PASAJERO A BORDO DE METRO SIN VIOLENCIA']),
        'metro-theft-violence': serialize_records(victims['ROBO A PASAJERO A BORDO DE METRO CON VIOLENCIA']),
        'metrobus-theft': serialize_records(victims['ROBO A PASAJERO A BORDO DE METROBUS SIN VIOLENCIA']),
        'metrobus-theft-violence': serialize_records(victims['ROBO A PASAJERO A BORDO DE METROBUS CON VIOLENCIA']),
        'microbus-theft': serialize_records(victims['ROBO A PASAJERO A BORDO DE PESERO COLECTIVO SIN VIOLENCIA']),
        'microbus-theft-violence': serialize_records(victims['ROBO A PASAJERO A BORDO DE PESERO COLECTIVO CON VIOLENCIA']),
        'pt-theft': serialize_records(victims['ROBO A PASAJERO A BORDO DE TRANSPORTE PÚBLICO SIN VIOLENCIA']),
        'pt-theft-violence': serialize_records(victims['ROBO A PASAJERO A BORDO DE TRANSPORTE PÚBLICO CON VIOLENCIA']),
        'light-train-theft': serialize_records(victims['ROBO A PASAJERO EN TREN LIGERO SIN VIOLENCIA']),
        'light-train-theft-violence': serialize_records(victims['ROBO A PASAJERO EN TREN LIGERO CON VIOLENCIA']),
        'suburban-train-theft': serialize_records(victims['ROBO A PASAJERO EN TREN SUBURBANO SIN VIOLENCIA']),
        'suburban-train-theft-violence': serialize_records(victims['ROBO A PASAJERO EN TREN SUBURBANO CON VIOLENCIA']),
        'trolleybus-theft': serialize_records(victims['ROBO A PASAJERO EN TROLEBUS SIN VIOLENCIA']),
        'trolleybus-theft-violence': serialize_records(victims['ROBO A PASAJERO EN TROLEBUS CON VIOLENCIA']),
        'rtp-bus-theft': serialize_records(victims['ROBO A PASAJERO EN RTP SIN VIOLENCIA']),
        'rtp-bus-theft-violence': serialize_records(victims['ROBO A PASAJERO EN RTP CON VIOLENCIA'])
    } }, status=200)
    
def serialize_records(records):
    return [{
        'id': record.id, 
        'location': record.coordinates.coords, 
        'felony-type': record.felony, 
        'category': record.category, 
        'date': record.date, 
        'time': record.time,
        'incident-type': record.incident_type() } for record in records]

def serialize_ageb_records(records):
    return [{
        'id': record.id, 
        'public_transport_assault_events_count': record.public_transport_assault_events_count, 
        'bicycle_theft_events_count': record.bike_theft_events_count, 
        'car_theft_events_count': record.car_theft_events_count, 
        'car_accessories_theft_events_count': record.car_accessories_theft_events_count, 
        'car_internal_belongings_theft_events_count': record.car_internal_belongings_theft_events_count, 
        'motorcycle_theft_events_count': record.motorcicle_theft_events_count, 
        'pedestrian_theft_events_count': record.pedestrian_theft_events_count, 
        'pedestrian_accidents_events_count': record.pedestrian_accidents_events_count, 
        'crash_accidents_events_count': record.crash_accidents_events_count, 
        'motorcycle_accidents_events_count': record.motorcicle_accidents_events_count, 
        'bicycle_accidents_events_count': record.bike_accidents_events_count, 
        'geometry': record.geometry.coords,
        'centroid': [record.geometry.centroid.x, record.geometry.centroid.y] } for record in records]

def serialize_ageb_detail_records(ageb_record, reports):
    return {
        'id': ageb_record.id,
        'centroid': [ageb_record.geometry.centroid.x, ageb_record.geometry.centroid.y],
        'incidents': serialize_records(reports)
    }