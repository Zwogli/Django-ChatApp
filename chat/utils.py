from django.core import serializers


def isRequestPost(request):
    #Query by POST methode, Query = dt. Abfrage
    return request.method == 'POST'


def serializeJson(request, object):
    #Creates JSON-Object
    return {
            'pk': object.pk,
            'fields': {
                'text': object.text,
                'created_at': object.created_at,
                'chat': object.chat.id,
                'author': object.author.id,
                'receiver': object.receiver.id,
                'author_name': request.user.username
            }
        }