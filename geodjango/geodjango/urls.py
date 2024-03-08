from django.contrib import admin
from django.urls import path
from world import views
from world import api
from world import conversations

urlpatterns = [
    path('admin/', admin.site.urls),
    path('stolen-bikes', api.stolen_bikes),
    path('transit-incidents', api.transit_incidents),
    path('public-transport-incidents', api.public_transport_incidents),
    path('categories/', views.categories),
    path('agebs/', api.agebs),
    path('agebs/<int:ageb_id>', api.ageb_details),
    path('conversations', conversations.ask_to_pdf),
    path('conversations/<uuid:device_id>/details/<str:use_case>', conversations.details)
]