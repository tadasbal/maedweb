from multiprocessing import context
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from django.urls import reverse
from .apis import retrieve_img, retrieve_all_documents, retrieve_one_document, upload_image_s3, add_restaurant, category_filter, search, user_activities, update_document, delete_image_s3, delete_document
from .models import Restaurant, Categories
import requests
from requests.auth import HTTPBasicAuth
import logging
from django.template.defaulttags import register

@register.filter
def get_range(value):
    return range(value)

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
    my_documents = retrieve_all_documents('maed-restaurants')
    categories = Categories()

    for document in my_documents:
        document['id'] = document.pop('_id')

    context['my_documents'] = my_documents
    context['restaurant_categories'] = categories.restaurant_categories
    return render(request, 'catalog/restaurants.html', context)

def entertainment(request):
    context = {}
    my_documents = retrieve_all_documents('maed-entertainment')
    categories = Categories()

    for document in my_documents:
        document['id'] = document.pop('_id')

    context['my_documents'] = my_documents
    context['entertainment_categories'] = categories.entertainment_categories
    return render(request, 'catalog/entertainment.html', context)

def events(request):
    context = {}
    my_documents = retrieve_all_documents('maed-events')
    categories = Categories()

    for document in my_documents:
        document['id'] = document.pop('_id')

    context['my_documents'] = my_documents
    context['event_categories'] = categories.event_categories
    return render(request, 'catalog/events.html', context)

def about_activity(request, activities, document_id):
    context = {}
    if activities == 'restaurants':
        req_document = retrieve_one_document(document_id, 'maed-restaurants')
    elif activities == 'entertainment': 
        req_document = retrieve_one_document(document_id, 'maed-entertainment')
    elif activities == 'events': 
        req_document = retrieve_one_document(document_id, 'maed-events')
    context['document'] = req_document
    context['document_id'] = document_id
    context['activities'] = activities
    return render(request, 'catalog/about_restaurant.html', context)

def search_request(request, activities):
    if request.method == 'POST':
        searchtxt = request.POST['search']
        req_documents = search(searchtxt, activities)
        request.session['req_documents'] = req_documents
        return redirect('maedweb:activities_filtered', activities=activities)

def filter_request(request, activities):
    if request.method == 'POST':
        selected_categories = request.POST.getlist('filter_checkbox')
        req_documents = category_filter(selected_categories, activities)
        request.session['req_documents'] = req_documents
        return redirect('maedweb:activities_filtered', activities=activities)

def activities_filtered(request, activities):
    context = {}
    categories = Categories()
    req_documents = request.session['req_documents']
    context['req_documents'] = req_documents
    context['categories'] = categories
    context['activities'] = activities
    return render(request, 'catalog/restaurants_filtered.html', context) 

def my_activities(request, username):
    context = {}
    categories = Categories
    restaurant_documents = user_activities(username, 'maed-restaurants')
    events_documents = user_activities(username, 'maed-events')
    entertainment_documents = user_activities(username, 'maed-entertainment')
    user_documents = restaurant_documents + events_documents + entertainment_documents
    context['user_documents'] = user_documents
    context['categories'] = categories
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
        add_restaurant(restaurant, form['new-activity-type'])

        return redirect('maedweb:my_activities', username=username)

def edit_activity_request(request, username, document_id, database):
    if request.method == 'POST':
        document = retrieve_one_document(document_id, database)
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
            restaurant.image_url = ''

        update_document(restaurant, document, database)

        return redirect('maedweb:my_activities', username=username)

def delete_activity_request(request, username, document_id, database):
    if request.method == 'POST':
        document = retrieve_one_document(document_id, database)
        delete_image_s3(document['image_url'])
        delete_document(document_id, database)
        return redirect('maedweb:my_activities', username=username)


