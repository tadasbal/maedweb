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
    path('entertainment', view=views.entertainment, name='entertainment'),
    path('events', view=views.events, name='events'),
    path('<str:activities>/filtered', view=views.activities_filtered, name='activities_filtered'),
    path('<str:activities>/filter', view=views.filter_request, name='filter_request'),
    path('<str:activities>/search', view=views.search_request, name='search_request'),
    path('myactivities/<str:username>', view=views.my_activities, name='my_activities'),
    path('<str:activities>/<str:document_id>', view=views.about_activity, name='about_activity'),
    path('myactivities/<str:username>/new', view=views.new_activity_request, name='new_activity_request'),
    path('myactivities/<str:username>/<str:document_id>/<str:database>/edit', view=views.edit_activity_request, name='edit_activity_request'),
    path('myactivities/<str:username>/<str:document_id>/<str:database>/delete', view=views.delete_activity_request, name='delete_activity_request'),
    path('loginrequest', views.login_request, name='login_request'),
    path('registration', views.registration_request, name='registration'),
    path('logout', views.logout_request, name='logout'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)