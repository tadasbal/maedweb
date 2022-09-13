from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'maedweb'
urlpatterns = [
    path('', view=views.index, name='index'),
    path('restaurants/image/<str:document_id>/<str:image_name>', view=views.show_image, name='showimage'),
    path('login', view=views.login_page, name='login'),
    path('register', view=views.register_page, name='register'),
    path('restaurants', view=views.restaurants, name='restaurants'),
    path('restaurants/filtered', view=views.restaurants_filtered, name='restaurants_filtered'),
    path('restaurants/filter', view=views.filter_request, name='filter_request'),
    path('restaurants/search', view=views.search_request, name='search_request'),
    path('restaurants/<str:document_id>', view=views.about_restaurant, name='about_restaurant'),
    path('myactivities/<str:username>', view=views.my_activities, name='my_activities'),
    path('myactivities/<str:username>/new', view=views.new_activity_request, name='new_activity_request'),
    path('myactivities/<str:username>/<str:document_id>/edit', view=views.edit_activity_request, name='edit_activity_request'),
    path('myactivities/<str:username>/<str:document_id>/delete', view=views.delete_activity_request, name='delete_activity_request'),
    path('loginrequest', views.login_request, name='login_request'),
    path('registration', views.registration_request, name='registration'),
    path('logout', views.logout_request, name='logout'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)