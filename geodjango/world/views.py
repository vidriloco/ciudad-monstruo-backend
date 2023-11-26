from django.http import JsonResponse
from django.template import loader

def index(request):
    data = {
        'name': 'John Doe',
        'age': 30,
        'email': 'john.doe@.com'
    }
    return JsonResponse(data, status=200)