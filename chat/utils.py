from django.core import serializers


def isRequestPost(request):
    #Query by POST methode, Query = dt. Abfrage
    return request.method == 'POST'


def serializeJson(request, object):
    # Convert dateobject to datetime-Objekt
    created_at_datetime = object.created_at
    # Convert dateobject to desired format
    formatted_created_at = created_at_datetime.strftime('%B %d, %Y')
    #Creates JSON-Object
    return {
            'pk': object.pk,
            'fields': {
                'text': object.text,
                'created_at': formatted_created_at,
                'chat': object.chat.id,
                'author': object.author.id,
                'receiver': object.receiver.id,
                'author_name': request.user.username
            }
        }