from multiprocessing import context
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from django.urls import reverse
from .apis import retrieve_img, retrieve_all_documents
import requests
from requests.auth import HTTPBasicAuth
import logging

logger = logging.getLogger(__name__)

# Create your views here.
# def show_image(request, document_id, image_name):
#     image = retrieve_img(document_id, image_name)

#     return HttpResponse(image, content_type="image/jpg")

def show_image(request, document_id, image_name):
    image = retrieve_img(document_id, image_name)
    return HttpResponse(image, content_type="image/jpg")


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
    context = {}
    converted_documents = []
    my_documents = retrieve_all_documents()
    for document in my_documents:
        converted_document = {}
        converted_document['id'] = document['_id']
        converted_document['name'] = document['name']
        converted_document['categories'] = document['categories']

        for img_name in document['_attachments']:
            images = []
            images.append(img_name)
            converted_document['images'] = images
        converted_document['main_image'] = images[0]
        converted_documents.append(converted_document)
    context['converted_documents'] = converted_documents
    return render(request, 'catalog/restaurants.html', context)

def about_restaurant(request, document_id):
    context = {}
    documents = retrieve_all_documents()
    for document in documents:
        if document['_id'] == document_id:
            req_document = document
            break
    for img_name in req_document['_attachments']:
        images = []
        images.append(img_name)
    context['document'] = req_document
    context['main_image'] = images[0]
    context['document_id'] = document_id
    return render(request, 'catalog/about_restaurant.html', context)

def filter_request(request):
    if request.method == 'POST':
        selected_categories = request.POST.getlist('filter_checkbox')
        request.session['selected-categories'] = selected_categories
        return redirect('maedweb:restaurants_filtered')

def restaurants_filtered(request):
    context = {}
    req_documents = []
    selected_categories = request.session['selected-categories']
    documents = retrieve_all_documents()
    for document in documents:
        for category in selected_categories:
            if category in document['categories']:
                req_documents.append(document)
                break
    for document in req_documents:
        document['id'] = document.pop('_id')
        document['attachments'] = document.pop('_attachments')
        images = list(document['attachments'].keys())
        document['main_image'] = images[0]
    context['req_documents'] = req_documents
    return render(request, 'catalog/restaurants_filtered.html', context) 

def my_activities(request):
    return render(request, 'catalog/my_activities.html')

