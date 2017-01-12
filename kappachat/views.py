from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


@login_required
def index(request):
    return render(request, "home.html")


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            messages.add_message(request, messages.error, "Invalid username or password.")
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
