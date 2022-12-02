"""Django views"""

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User, Group
from catalog.modules.databases.cloudant import *
from catalog.modules.databases.aws import *
from .models import Activity, Categories
import logging
from django.template.defaulttags import register

@register.filter
def get_range(value):
    """Get range. Used in about_activity.html to render a specific number of stars for ratings"""
    return range(value)

logger = logging.getLogger(__name__)

def index(request):
    """Render index page"""
    return render(request, 'catalog/index.html')

def login_page(request):
    """Render login page"""
    return render(request, 'catalog/login.html')

def login_request(request):
    """Login request if user tries to login"""
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
    """Logout request if user tries to logout"""
    logout(request)
    return redirect('maedweb:index')

def register_page(request):
    """Render register page"""
    return render(request, 'catalog/register.html')

def registration_request(request):
    """Register request if user tries to register"""
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
    """Retrieve all restaurants from cloudant and render restaurants page """
    context = {}
    my_documents = retrieve_all_documents('maed-restaurants')
    categories = Categories()

    for document in my_documents:
        document['id'] = document.pop('_id')

    context['my_documents'] = my_documents
    context['categories'] = categories.restaurant_categories
    context['displayed_categories'] = ["Most Popular", "Fast Food", "Italian", "Pasta"]
    context['activities'] = "restaurants"
    return render(request, 'catalog/activities.html', context)

def entertainment(request):
    """Retrieve all entertainment from cloudant and render entertainment page """
    context = {}
    my_documents = retrieve_all_documents('maed-entertainment')
    categories = Categories()

    for document in my_documents:
        document['id'] = document.pop('_id')

    context['my_documents'] = my_documents
    context['categories'] = categories.entertainment_categories
    context['displayed_categories'] = ["Most Popular", "Active", "Outdoors", "Indoors"]
    context['activities'] = "entertainment"

    return render(request, 'catalog/activities.html', context)

def events(request):
    """Retrieve all events from cloudant and render events page """
    context = {}
    my_documents = retrieve_all_documents('maed-events')
    categories = Categories()

    for document in my_documents:
        document['id'] = document.pop('_id')

    context['my_documents'] = my_documents
    context['categories'] = categories.event_categories
    context['displayed_categories'] = ["Most Popular", "Concert", "Indoors", "Active"]
    context['activities'] = "events"

    return render(request, 'catalog/activities.html', context)

def about_activity(request, activities, document_id):
    """Retrieve a specific document from cloudant and render about activity page"""
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
    return render(request, 'catalog/about_activity.html', context)

def search_request(request, activities):
    """Search request if user tries to search for specific activities"""
    if request.method == 'POST':
        searchtxt = request.POST['search']
        req_documents = search(searchtxt, activities)
        request.session['req_documents'] = req_documents
        return redirect('maedweb:activities_filtered', activities=activities)

def filter_request(request, activities):
    """Filter request if user tries to filter activity categories"""
    if request.method == 'POST':
        selected_categories = request.POST.getlist('filter_checkbox')
        req_documents = category_filter(selected_categories, activities)
        request.session['req_documents'] = req_documents
        return redirect('maedweb:activities_filtered', activities=activities)

def activities_filtered(request, activities):
    """Render activities after they have been filtered after filter or search request"""
    context = {}
    categories = Categories()
    req_documents = request.session['req_documents']
    context['req_documents'] = req_documents
    context['categories'] = categories
    context['activities'] = activities
    return render(request, 'catalog/activities_filtered.html', context) 

def my_activities(request, username):
    """Render all of user activities"""
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
    """User request to create new activity"""
    if request.method == 'POST':
        form = request.POST

        image = request.FILES['image']
        image_url = upload_image_s3(image, form['company-name'])

        activity = Activity(
            user = username,
            type = form['new-activity-type'],
            name = form['company-name'],
            categories = request.POST.getlist('categories'),
            reviews = {"Overall":0, "Food":0, "Price":0, "Service":0, "Place":0},
            contacts = {"address":form['address'], "phone":form['phone'], "email":form['email'], "website":form['website']},
            details = {"about":form['about-activity'], "features":form['features']},
            menu_link = form['menu-link'],
            image_url = image_url)

        add_activity(activity)

        return redirect('maedweb:my_activities', username=username)

def edit_activity_request(request, username, document_id, database):
    """User request to edit activity"""
    if request.method == 'POST':
        document = retrieve_one_document(document_id, database)
        form = request.POST

        activity = Activity
        activity.name = form['company-name']
        activity.categories = request.POST.getlist('categories')
        activity.contacts = {"address":form['address'], "phone":form['phone'], "email":form['email'], "website":form['website']}
        activity.details = {"about":form['about-activity'], "features":form['features']}
        activity.menu_link = form['menu-link']

        try:
            image = request.FILES['image']
            delete_image_s3(document['image_url'])
            image_url = upload_image_s3(image, activity.name)
            activity.image_url = image_url
        except:
            print('No new image attached')
            activity.image_url = ''

        update_document(activity, document, database)

        return redirect('maedweb:my_activities', username=username)

def delete_activity_request(request, username, document_id, database):
    """User request to delete activity"""
    if request.method == 'POST':
        document = retrieve_one_document(document_id, database)
        delete_image_s3(document['image_url'])
        delete_document(document_id, database)
        return redirect('maedweb:my_activities', username=username)

# def error_404(request, exception):
#         data = {}
#         return render(request,'catalog/404.html', data)

# def error_500(request):
#         data = {}
#         return render(request,'catalog/500.html', data)
