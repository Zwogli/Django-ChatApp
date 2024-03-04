from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Message, Chat
from .forms import RegisterUserForm
from .utils import *

"""
chat_id_number = static id for test chat
"""
chat_id_number = 1


# Create your views here.
"""
@login_required(login_url='/login_user/'):
Check if user is logged in, if not refers to login.
"""
@login_required(login_url='/login/')
def chat(request):
    """
    Render content into chat page.
    """
    if isRequestPost(request):
        """
        Is request.method == 'POST' create a new message and return an Json-Object
        testChat = static Chatroom
        """                                 
        testChat = Chat.objects.get(id=chat_id_number)
        new_message = createMessage(request, testChat)
        serialized_message = serializeJson(request, new_message)
        return JsonResponse(serialized_message, safe=False)
    chat_messages = filterChatMessages(chat_id_number)
    """
    chat_messages returns Array
    """
    return render(                                                  
        request, 
        'chat/chat.html', 
        {'chat_messages': chat_messages}
    )


def login_user(request):
    redirect = request.GET.get('next')
    if isRequestPost(request):
        user = authenticate(                                        #check login inputs
            username = request.POST.get('username'), 
            password = request.POST.get('password')
        )
        if isUserExist(user):                                        #Succesfully login, directs URL
            login(request, user)
            if redirect=='next':
                return HttpResponseRedirect(
                    request.POST.get('redirect')
                )
            else:
                chat_messages = filterChatMessages(chat_id_number) 
                return render(
                    request, 'chat/chat.html', 
                    {'chat_messages': chat_messages}
                )
        else:
            #Incorrect login, redirects:
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
            chat_messages = filterChatMessages(chat_id_number)
            return render(
                request, 
                'chat/chat.html', 
                {'chat_messages': chat_messages}
            )
    else:
        form = RegisterUserForm()       #Load custom register form 'form.py'
    return render(request, 'auth/registry.html', {'form': form,})