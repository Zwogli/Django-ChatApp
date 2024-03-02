from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Message, Chat, RegistryUser


# Create your views here.
@login_required(login_url='/login/')                                #Verweist auf die Login Seite
def index(request):
    if request.method == 'POST':                                    #Abfrage nach POST methode
        testChat = Chat.objects.get(id=1)                           #Erstellt statischen Chatroom
        Message.objects.create(                                     #Erstell Chat mit folgenden Inhalt ()
            text=request.POST['messagefield'], 
            chat=testChat, 
            author=request.user, 
            receiver=request.user
        )    
    chat_messages = Message.objects.filter(chat__id=1)              #chat__id=1 = object__mit der id 1 => gibt ein Array zurück
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
    messages.success(request, ("You Have Been Logged Out."))
    return redirect('login')
    


def registry_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            chat_messages = Message.objects.filter(chat__id=1)
            return render(
                request, 
                'chat/index.html', 
                {'chat_messages': chat_messages}
            )
        # return render(
        #     request, 
        #     'auth/login.html', 
        #     {'successfulRegistration': True}, 
        # )
    else:
        form = UserCreationForm()
    return render(request, 'auth/registry.html', {'form': form,})