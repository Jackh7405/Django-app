from . import views
from django.urls import path

app_name = 'itreporting'

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home-alias'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('modules/', views.ModuleListView.as_view(), name='module-list'),
    path('modules/<str:code>/', views.ModuleDetailView.as_view(), name='module-detail'),
    path('modules/<str:code>/register/', views.register_module, name='module-register'),
    path('modules/<str:code>/unregister/', views.unregister_module, name='module-unregister'),
    path('my-registrations/', views.my_registrations, name='my-registrations'),
]