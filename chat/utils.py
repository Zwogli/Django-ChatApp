from .models import Message


def isRequestPost(request):
    #Query by POST methode, Query = dt. Abfrage
    """
    :param request: HTTP request object.
    :type request: HttpRequest
    
    Check request method:
    
    :return: True if the methode is 'POST'
    :rtype: bool
    """
    return request.method == 'POST'


def isUserExist(user):
    return user is not None


def createMessage(request, chat):
    """
    Create a Message object with the following parameters:

    :param request: HTTP request object.
    :type request: HttpRequest
    :param chat: Chat ID.
    :type chat: int

    This function creates a Message object with attributes such as text, chat, author, and receiver.
    """
    return (Message.objects.create(
            text=request.POST['messageField'], 
            chat=chat, 
            author=request.user, 
            receiver=request.user
        )
    )


def serializeJson(request, object):
    """Convert dateobject to datetime-Objekt"""
    created_at_datetime = object.created_at
    """Convert dateobject to desired format"""
    formatted_created_at = created_at_datetime.strftime('%B %d, %Y')
    """
    :return: created JSON-Object
    """
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
    
    
def filterChatMessages(id_number):
    """returns an array from chat__id=chat id number"""
    return Message.objects.filter(chat__id=id_number)