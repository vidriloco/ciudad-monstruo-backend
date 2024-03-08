import requests
from django.http import JsonResponse
import os
import time
import re
from .models import Conversation
from django.utils import timezone
from django.core.serializers import serialize
import re

API_KEY="sec_a42axrOb43kzQDonkpxySMtNOYhRc2eO"

def ask_to_pdf(request):
    query = request.GET.get('query')
    case = request.GET.get('case')
    device_id = request.GET.get('device_id')
    use_history = request.GET.get('use_history')
    
    if query is None:
        return JsonResponse({}, status=400)
    
    pdf_id = pdf_id_for_use_case(case)
    
    if pdf_id is None:
        pdf_id = get_pdf_id_for(pdf_url_for_use_case(case))
    
    userMessage = Conversation(date=timezone.now(), message=query, source="U", deviceID=device_id, useCase=case)
    if userMessage.save() == None:
        history = Conversation.objects.filter(deviceID=device_id, useCase=case).order_by('date')[:3] if use_history else []
        response = ask_question(pdf_id, query, history)
        
        if response.status_code == 200:
            content = response.json()['content']
            
            assistantMessage = Conversation(date=timezone.now(), message=content, source="A", deviceID=device_id, useCase=case)
            assistantMessage.save()
            
            return JsonResponse({'answer': parse_string(content)}, status=200)
        else:
            return None
    else:
        return JsonResponse({'error': "No recibimos tu mensaje, intenta de nuevo"}, status=404)

def details(request, device_id, use_case):    
    conversations = Conversation.objects.filter(deviceID=device_id, useCase=use_case).order_by('date')
    values = conversations.values(*['date', 'message', 'source'])
    
    pattern = r'\[Página (\d+)\]'
    
    parsed_values = []
    for entry in values:
        entry['message'] = parse_string(re.sub(pattern, replace_page_number, entry['message']))
        parsed_values.append(entry)
            
    return JsonResponse({ 'collection': parsed_values }, status=200)
    

def replace_page_number(match):
    page_number = match.group(1)
    return f"[P{page_number}]"
    
def parse_string(input_string):
    pattern = r'([^[]+)(?:\s*\[P(\d+)\]\s*|$)'
    matches = re.finditer(pattern, input_string)
    result = []

    for match in matches:
        result.append(match.group(1).strip())
        if match.group(2) is not None:
            result.append(f"$ {match.group(2)}")

    return result

def ask_question(pdf_id, question, history):
    headers = {
        'x-api-key': API_KEY,
        "Content-Type": "application/json",
    }
    
    historic_messages = []
    
    for item in history:
        historic_messages.append({
            'role': 'user' if item.source == "U" else "assistant",
            'content': item.message
        })
    
    data = {
        'referenceSources': True,
        'sourceId': pdf_id,
        'messages': historic_messages if historic_messages else {
            'role': "user",
            'content': question,
        }
    }
    
    print(data)
    
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
    