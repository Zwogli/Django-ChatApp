from datetime import date
from django.db import models


# Create your models here.

class Chat(models.Model):    
    created_at = models.DateField(default=date.today)

class Message(models.Model):
    text = models.CharField(max_length=500)    
    created_at = models.DateField(default=date.today)    
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)    
    author = models.CharField(max_length=50)    
    receiver = models.CharField(max_length=50)