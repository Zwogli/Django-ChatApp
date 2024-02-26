from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Message, Chat


# Create your views here.
@login_required(login_url='/login/')                                #Verweist auf die Login Seite
def index(request):
    if request.method == 'POST':                                    #Abfrage nach POST methode
        print("Receive data " + request.POST['messagefield'])
        testChat = Chat.objects.get(id=1)                           #Erstellt statischen Chatroom
        Message.objects.create(                                     #Erstell Chat mit folgenden Inhalt ()
            text=request.POST['messagefield'], 
            chat=testChat, 
            author=request.user, 
            receiver=request.user
        )    
    chat_messages = Message.objects.filter(chat__id=1)              #chat__id=1 = object__mit der id 1 => gibt ein Array zurück
    print(chat_messages)
    #Rendert URL chat/index.html mit Inhalt aus der Datenbank 'chat_message':
    return render(                                                  
        request, 
        'chat/index.html', 
        {'chat_messages': chat_messages}
    )


def login_user(request):
    redirect = request.GET.get('next')
    if request.method == 'POST':
        user = authenticate(                                        #check login inputs
            username = request.POST.get('username'), 
            password = request.POST.get('password')
        )
        if user is not None:                                        #Succesfully login, directs URL
            login(request, user)
            if redirect=='next':
                return HttpResponseRedirect(
                    request.POST.get('redirect')
                )
            else:
                chat_messages = Message.objects.filter(chat__id=1)
                return render(
                    request, 'chat/index.html', 
                    {'chat_messages': chat_messages}
                )
        else:
            #Fehlerhater Login, leitet zurück:
            return render(
                request, 
                'auth/login.html', 
                {'wrongPassword': True}, 
                {'redirect':redirect}
            )
    return render(request, 'auth/login.html', {'redirect': redirect})


def logout_user(request):
    logout(request)
    pass


def registry_view(request):
    if request.method == 'POST':
        user = User.objects.create_user(
            username=request.POST.get('username'),
            email=request.POST.get('email'),
            password=request.POST.get('password')
        )
        user.save()
        return render(
            request, 
            'auth/login.html', 
            {'successfulRegistration': True}, 
        )
    return render(request, 'auth/registry.html')