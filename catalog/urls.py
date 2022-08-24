from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'maedweb'
urlpatterns = [
    path('', view=views.index, name='index'),
    path('login', view=views.login_page, name='login'),
    path('register', view=views.register_page, name='register'),
    path('restaurants', view=views.restaurants, name='restaurants'),
    path('loginrequest', views.login_request, name='login_request'),
    path('registration', views.registration_request, name='registration'),
    path('logout', views.logout_request, name='logout'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)