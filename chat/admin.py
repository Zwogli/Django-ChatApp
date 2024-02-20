from django.contrib import admin

from .models import Chat, Message

# Definiert die Anzeige im Dashboard
class MessageAdmin(admin.ModelAdmin):    
    fields = ('chat', 'text','created_at', 'author', 'receiver')    
    list_display = ('created_at', 'author', 'text', 'receiver')    
    search_fields = ('text',)

# Register your models here.
admin.site.register(Message, MessageAdmin)
admin.site.register(Chat)