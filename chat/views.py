from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Message, Chat
from .forms import RegisterUserForm
from .utils import *


# Create your views here.
@login_required(login_url='/login_user/')                           #Refers to login page
def index(request):
    if isRequestPost(request):                                    
        testChat = Chat.objects.get(id=1)                           #Creates static Chatroom
        new_message = Message.objects.create(                       #Create a Chat with following elements (new_message = )
            text=request.POST['messageField'], 
            chat=testChat, 
            author=request.user, 
            receiver=request.user
        )
        serialized_message = serializeJson(request, new_message)             #json array from object
        print("serialized_message :", serialized_message)
        return JsonResponse(serialized_message, safe=False)   #[1:-1] remove substring
    chat_messages = Message.objects.filter(chat__id=1)              #chat__id=1 = object__mit der id 1 => returns an Array
    #Rendert URL chat/index.html mit Inhalt aus der Datenbank 'chat_message':
    return render(                                                  
        request, 
        'chat/index.html', 
        {'chat_messages': chat_messages}
    )


def login_user(request):
    redirect = request.GET.get('next')
    if isRequestPost(request):
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
            #Incorrect login, redirects:
            return render(
                request, 
                'auth/login_user.html', 
                {'wrongPassword': True}, 
                {'redirect':redirect}
            )
    return render(request, 'auth/login_user.html', {'redirect': redirect})


def logout_user(request):
    logout(request)
    messages.success(request, ("You Have Been Logged Out."))
    return redirect('login_user')
    


def registry_user(request):
    if isRequestPost(request):
        form = RegisterUserForm(request.POST)
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
    else:
        form = RegisterUserForm()       #Load custom register form 'form.py'
    return render(request, 'auth/registry_user.html', {'form': form,})