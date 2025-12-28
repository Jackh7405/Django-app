from . import views
from django.urls import path

app_name = 'itreporting'

urlpatterns = [
    # Basic pages
    path('', views.home, name='home'),
    path('home/', views.home, name='home-alias'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    
    # Module pages (new for Module Registration System)
    path('modules/', views.ModuleListView.as_view(), name='module-list'),
    path('modules/<str:code>/', views.ModuleDetailView.as_view(), name='module-detail'),
    
    # We'll add more URLs as we build:
    # - Course-specific module lists
    # - Registration/unregistration endpoints
    # - My Registrations page
]