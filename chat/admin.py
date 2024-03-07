from django.contrib import admin

from .models import Chat, Message

# Definiert die Anzeige im Dashboard
class MessageAdmin(admin.ModelAdmin):    
    """
    Defines which information should be displayed in the admin dashboard
    
    :field: list
    :list_display: list
    :search_fields: list
    """
    fields = ('chat', 'text','created_at', 'author', 'receiver')    
    list_display = ('created_at', 'author', 'text', 'receiver')    
    search_fields = ('text',)

# Register your models here.
admin.site.register(Message, MessageAdmin)
admin.site.register(Chat)