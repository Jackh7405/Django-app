from . import views
from django.urls import path

app_name = 'itreporting'

urlpatterns = [

    path('', views.home, name = 'home'),
    path('contact/', views.contact, name = 'contact'),
    path('about/', views.about, name = 'about'),
    path('home/', views.home, name = 'home-alias')
]