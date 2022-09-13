from multiprocessing import context
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from django.urls import reverse
from .apis import retrieve_img, retrieve_all_documents, retrieve_one_document, upload_image_s3, add_restaurant, category_filter, search, user_activities, update_document, delete_image_s3
from .models import Restaurant
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
    my_documents = retrieve_all_documents()
    for document in my_documents:
        document['id'] = document.pop('_id')
    # for document in my_documents:
    #     converted_document = {}
    #     converted_document['id'] = document['_id']
    #     converted_document['name'] = document['name']
    #     converted_document['categories'] = document['categories']

    #     for img_name in document['_attachments']:
    #         images = []
    #         images.append(img_name)
    #         converted_document['images'] = images
    #     converted_document['main_image'] = images[0]
    #     converted_documents.append(converted_document)
    context['my_documents'] = my_documents
    return render(request, 'catalog/restaurants.html', context)

def about_restaurant(request, document_id):
    context = {}
    documents = retrieve_all_documents()
    for document in documents:
        if document['_id'] == document_id:
            req_document = document
            break
    # for img_name in req_document['_attachments']:
    #     images = []
    #     images.append(img_name)
    context['document'] = req_document
    # context['main_image'] = images[0]
    context['document_id'] = document_id
    return render(request, 'catalog/about_restaurant.html', context)

def search_request(request):
    if request.method == 'POST':
        searchtxt = request.POST['search']
        req_documents = search(searchtxt)
        request.session['req_documents'] = req_documents
        return redirect('maedweb:restaurants_filtered')

def filter_request(request):
    if request.method == 'POST':
        selected_categories = request.POST.getlist('filter_checkbox')
        req_documents = category_filter(selected_categories)
        request.session['req_documents'] = req_documents
        return redirect('maedweb:restaurants_filtered')

def restaurants_filtered(request):
    context = {}
    req_documents = request.session['req_documents']
    context['req_documents'] = req_documents
    return render(request, 'catalog/restaurants_filtered.html', context) 

def my_activities(request, username):
    context = {}
    user_documents = user_activities(username)
    context['user_documents'] = user_documents
    return render(request, 'catalog/my_activities.html', context)

def new_activity_request(request, username):
    if request.method == 'POST':
        form = request.POST

        image = request.FILES['image']
        image_url = upload_image_s3(image, form['company-name'])

        restaurant = Restaurant
        restaurant.user = username 
        restaurant.name = form['company-name']
        restaurant.categories = request.POST.getlist('categories')
        restaurant.reviews = {"Overall":0, "Food":0, "Price":0, "Service":0, "Place":0}
        restaurant.contacts = {"address":form['address'], "phone":form['phone'], "email":form['email'], "website":form['website']}
        restaurant.details = {"about":form['about-activity'], "features":form['features']}
        restaurant.menu_link = form['menu-link']
        restaurant.image_url = image_url
        add_restaurant(restaurant)

        return redirect('maedweb:my_activities', username=username)

def edit_activity_request(request, username, document_id):
    if request.method == 'POST':
        document = retrieve_one_document(document_id)
        form = request.POST

        restaurant = Restaurant
        restaurant.name = form['company-name']
        restaurant.categories = request.POST.getlist('categories')
        restaurant.contacts = {"address":form['address'], "phone":form['phone'], "email":form['email'], "website":form['website']}
        restaurant.details = {"about":form['about-activity'], "features":form['features']}
        restaurant.menu_link = form['menu-link']

        try:
            image = request.FILES['image']
            delete_image_s3(document['image_url'])
            image_url = upload_image_s3(image, restaurant.name)
            restaurant.image_url = image_url
        except:
            print('No new image attached')

        update_document(restaurant, document)

        return redirect('maedweb:my_activities', username=username)

def delete_activity_request(request, username, document_id):
    if request.method == 'POST':
        document = retrieve_one_document(document_id)
        delete_image_s3(document['image_url'])
        document.delete()
        return redirect('maedweb:my_activities', username=username)


