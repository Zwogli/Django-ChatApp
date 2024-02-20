from django.shortcuts import render

from .models import Message, Chat

# Create your views here.
def index(request):
    if request.method == 'POST':
        print("Receive data " + request.POST['messagefield'])
        testChat = Chat.objects.get(id=1)       #Erstellt statischen Chatroom
        Message.objects.create(
            text=request.POST['messagefield'], 
            chat=testChat, 
            author=request.user, 
            receiver=request.user
        )    #Erstell Chat mit folgenden Inhalt ()
    chat_messages = Message.objects.filter(chat__id=1)    #chat__id=1 = object__mit der id 1 => gibt ein Array zurück
    print(chat_messages)
    return render(request, 'chat/index.html', {'chat_messages': chat_messages})