import requests
from django.http import JsonResponse
import os
import time
import re

API_KEY="sec_a42axrOb43kzQDonkpxySMtNOYhRc2eO"

def ask_to_pdf(request):
    query = request.GET.get('query')
    case = request.GET.get('case')
    
    if query is None:
        return JsonResponse({}, status=400)
    
    pdf_id = pdf_id_for_use_case(case)
    
    if pdf_id is None:
        pdf_id = get_pdf_id_for(pdf_url_for_use_case(case))
    
    response = ask_question(pdf_id, query)
    
    time.sleep(5)
    #item = "es una indagación [P12] en la profunda conexión humana con el acto de [P13] correr. Hemos viajado a todos los [P14] continentes, donde nuestras protagonistas, [P15] corredoras de diferentes culturas y estratos sociales nos guiarán para descubrir el verdadero significado del deporte, uno que toca las fibras mismas de lo que nos hace humanos. Filmada en México, España, Grecia, Japón y Kenia."
    if response.status_code == 200:
        json = response.json()
        return JsonResponse({'answer': parse_string(json['content']), 'references': json['references'] }, status=200)
        #return JsonResponse({'answer': parse_string(item), 'references': {} }, status=200)
    else:
        return None

def parse_string(input_string):
    pattern = r'([^[]+)(?:\s*\[P(\d+)\]\s*|$)'
    matches = re.finditer(pattern, input_string)
    result = []

    for match in matches:
        result.append(match.group(1).strip())
        if match.group(2) is not None:
            result.append(f"$ {match.group(2)}")

    return result

def ask_question(pdf_id, question):
    headers = {
        'x-api-key': API_KEY,
        "Content-Type": "application/json",
    }

    data = {
        'referenceSources': True,
        'sourceId': pdf_id,
        'messages': [
            {
                'role': "user",
                'content': question,
            }
        ]
    }

    return requests.post('https://api.chatpdf.com/v1/chats/message', headers=headers, json=data)

def get_pdf_id_for(url):
    response = upload_pdf_from_url(url)

    if response.status_code == 200:
        return response.json()['sourceId']
    else:
        return None

def pdf_id_for_use_case(case):
    return {
        'motorized': 'src_epeRDqC8lTb2yMzytfL5v',
    }[case]

def pdf_url_for_use_case(case):
    return {
        'motorized': 'https://www.ssc.cdmx.gob.mx/storage/app/media/Transito/Actualizaciones/Reglamento-de-Transito-CDMX.pdf',
    }[case]
        
def upload_transit_document():
    headers = {
      'x-api-key': API_KEY,
      'Content-Type': 'application/json'
    }
    
    static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/pdf')
    file_absolute_path = os.path.join(static_dir, 'reglamento-transito-cdmx.pdf')
    
    files = [
        ('file', ('file', open(file_absolute_path, 'rb'), 'application/octet-stream'))
    ]
    
    return requests.post('https://api.chatpdf.com/v1/sources/add-file', headers=headers, files=files)
    
    
def upload_pdf_from_url(url):
    headers = {
      'x-api-key': API_KEY,
      'Content-Type': 'application/json'
    }
    data = {'url': url}

    return requests.post('https://api.chatpdf.com/v1/sources/add-url', headers=headers, json=data)
    