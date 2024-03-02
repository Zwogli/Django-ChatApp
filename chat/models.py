from datetime import date
from django.conf import settings
from django.db import models
from django import forms


# Create your models here.

class Chat(models.Model):    
    created_at = models.DateField(default=date.today)

class Message(models.Model):
    text = models.CharField(max_length=500)    
    created_at = models.DateField(default=date.today)    
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='chat_message_set', default=None, blank=True, null=True)    
    # author = models.CharField(max_length=50)    
    # receiver = models.CharField(max_length=50)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author_message_set')    
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='receiver_message_set')
    
    
class RegistryUser(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)