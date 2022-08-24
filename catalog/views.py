from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User, Group
import requests
from requests.auth import HTTPBasicAuth
import logging

logger = logging.getLogger(__name__)
# Create your views here.
def index(request):
    return render(request, 'catalog/index.html')

def login_page(request):
    return render(request, 'catalog/login.html')

def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['login-username']
        password = request.POST['login-password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('maedweb:index')
        else:
            context['message'] = "Invalid username, password or account type."
            return render(request, 'catalog/login.html', context)

def logout_request(request):
    logout(request)
    return redirect('maedweb:index')

def register_page(request):
    return render(request, 'catalog/register.html')

def registration_request(request):
    context = {}
    if request.method == 'POST':
        # Check if user exists
        username = request.POST['register-username']
        password = request.POST['register-password']
        first_name = request.POST['register-name']
        email = request.POST['register-email']
        group = request.POST['register-account-type']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, email=email,
                                            password=password)

            user_group = Group.objects.get(name=group) 
            user.groups.add(user_group)

            login(request, user)
            return redirect("maedweb:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'catalog/register.html', context)

def restaurants(request):
    return render(request, 'catalog/restaurants.html')
