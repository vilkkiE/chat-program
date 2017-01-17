from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from . import models, forms
from django.template.loader import render_to_string
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm


@login_required
def index(request):
    channels = models.Channel.objects.all()
    return render(request, "home.html", {'channels': channels})


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "login.html")


@login_required()
def logout_user(request):
    logout(request)
    return render(request, "login.html")


def register(request):
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return HttpResponseRedirect('/')
    else:
        user_form = UserCreationForm()
    return render(request, "register.html", {'user_form': user_form})


@login_required()
def create_channel(request):
    if request.method == 'POST':
        channel_form = forms.ChannelForm(request.POST)
        if channel_form.is_valid():
            channel = models.Channel(name=request.POST['name']).save()
        else:
            messages.error(request, "Invalid name.")
        return HttpResponseRedirect('/')


@login_required()
def join_channel(request):
    if request.method == 'POST':
        channel_name = request.POST['channel_name'][1:]
        channel = models.Channel.objects.get(name=channel_name)
        chat_messages = models.Message.objects.filter(channel=channel)
        channels = models.Channel.objects.all()
        html_to_return = render_to_string('chat.html', {'channel_name': channel_name, 'channels': channels, 'chat_messages': chat_messages}, request)
        return HttpResponse(html_to_return)


@login_required()
def send_message(request):
    if request.method == 'POST':
        channel_name = request.POST['channel_name'][1:]
        channel = models.Channel.objects.get(name=channel_name)
        message = models.Message(content=request.POST['message'], channel=channel, sentBy=request.user).save()
        return HttpResponse('Message sent')


@login_required()
def update_chat(request):
    if request.method == 'POST':
        channel_name = request.POST['channel_name'][1:]
        channel = models.Channel.objects.get(name=channel_name)
        chat_messages = models.Message.objects.filter(channel=channel)
        channels = models.Channel.objects.all()
        html_to_return = render_to_string('chat_window.html', {'channel_name': channel_name, 'channels': channels,
                                                               'chat_messages': chat_messages}, request)
        return HttpResponse(html_to_return)


@login_required()
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Password changed.')
            return HttpResponseRedirect('/')
    else:
        form = PasswordChangeForm(request.user)
    form.fields['old_password'].widget.attrs = {'class': 'form-control'}
    form.fields['new_password1'].widget.attrs = {'class': 'form-control'}
    form.fields['new_password2'].widget.attrs = {'class': 'form-control'}

    return render(request, "change_password.html", {'form': form})