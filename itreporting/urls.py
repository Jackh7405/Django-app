from . import views
from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView
app_name = 'itreporting'

urlpatterns = [

    path('', views.home, name = 'home'),
    path('contact/', views.contact, name = 'contact'),
    path('about/', views.about, name = 'about'),
    path('home/', views.home, name = 'home-alias'),
    path('report/', PostListView.as_view(), name = 'report'),
    path('issues/<int:pk>', PostDetailView.as_view(), name = 'issue-detail'),
    path('issues/new', PostCreateView.as_view(), name = 'issue-create'),
    path('issues/<int:pk>/update/', PostUpdateView.as_view(), name = 'issue-update'),
    path('issues/<int:pk>/delete/', PostDeleteView.as_view(), name = 'issue-delete'),
    path('issue/<str:username>', UserPostListView.as_view(), name = 'user-issues'),
]