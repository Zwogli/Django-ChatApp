from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import Message, Chat
from .forms import RegisterUserForm
from .utils import *

# import pdb #python debbuger

"""
chat_id_number = static id for test chat
"""
chat_id_number = 1


# Create your views here.


@login_required(login_url='/login/')        #Check if user is logged in, if not refers to login.
def chat(request):
    """
    If the request a POST method:
    
    :return JsonResponse: Sends an JSON back to the frontend
    :param  data: JSON-Oject
    :param  safe: bool False
    
    else:
    
    :return render: Render HTML with render() with:
    
    :param  request: HTTP request object.
    :param  template_name: url 'chat/chat.html'
    :param  dict: {'chat_messages': chat_messages}
    """
    if isRequestPost(request):                             
        testChat = Chat.objects.get(id=chat_id_number)
        new_message = createMessage(request, testChat)
        serialized_message = serializeJson(request, new_message)
        return JsonResponse(serialized_message, safe=False)
    chat_messages = filterChatMessages(chat_id_number)
    return render(                                                  
        request, 
        'chat/chat.html', 
        {'chat_messages': chat_messages}
    )


def login_user(request):
    """
    If isRequestPost(request): 
    
    Check the Post methode and login inputs
    
    If isUserExist(user):
    
    Succesfully login, directs URL and render chat_messages
    
    else:
    
    Incorrect login, redirects to login page.
    """
    redirect_extract = request.GET.get('next')
    if isRequestPost(request):
        user = authenticate(
            username = request.POST.get('username'), 
            password = request.POST.get('password')
        )
        if isUserExist(user):
            login(request, user)
            if redirect_extract=='next':
                return HttpResponseRedirect(
                    request.POST.get('redirect_extract')
                )
            else:
                return redirect('chat')
        else:
            return render(
                request, 
                'auth/login.html', 
                {'wrongPassword': True}, 
                {'redirect':redirect_extract}
            )
    return render(request, 'auth/login.html', {'redirect': redirect_extract})


def logout_user(request):
    """
    Logged out the logged in user and response a message.
    
    :return: Redirect to login URL
    """
    logout(request)
    messages.success(request, ("You Have Been Logged Out."))
    return redirect('login_user')


def registry_user(request):
    """
    :form: Creates a form registration
    
    Clean username and password

    :user: authenticate
    
    Login as authenticate user and render chat.html with messages

    else:

    Load custom register form 'form.py'

    :redirect: to registry page
    """
    if isRequestPost(request):
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('chat')
    else:
        form = RegisterUserForm()
    return render(request, 'auth/registry.html', {'form': form,})