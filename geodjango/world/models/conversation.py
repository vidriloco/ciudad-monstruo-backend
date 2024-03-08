from django.contrib.gis.db import models

class Conversation(models.Model):
    date = models.DateTimeField()
    message = models.TextField()
    source = models.CharField(1)
    deviceID = models.UUIDField()
    useCase = models.CharField(15)