from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Module  # Only import Module now
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import DeleteView
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User, Group

# ============================================================================
# BASIC PAGES (Home, About, Contact)
# ============================================================================

def home(request):
    """Home page - landing page for the application"""
    context = {
        'title': 'Welcome',
        'courses': Group.objects.all()  # Show list of courses on home
    }
    return render(request, 'itreporting/home.html', context)


def about(request):
    """About Us page"""
    return render(request, 'itreporting/about.html', {'title': 'About Us'})


def contact(request):
    """Contact Us page"""
    return render(request, 'itreporting/contact.html', {'title': 'Contact Us'})


# ============================================================================
# MODULE VIEWS (New - for Module Registration System)
# ============================================================================

class ModuleListView(ListView):
    """
    Display list of all modules
    Later we can filter by course
    """
    model = Module
    template_name = 'itreporting/module_list.html'
    context_object_name = 'modules'
    ordering = ['code']
    paginate_by = 10  # Pagination requirement


class ModuleDetailView(DetailView):
    """
    Display details of a single module
    Students can register/unregister from this page
    """
    model = Module
    template_name = 'itreporting/module_detail.html'
    # We'll use 'code' instead of 'pk' in URLs (intermediate requirement)
    slug_field = 'code'
    slug_url_kwarg = 'code'


# ============================================================================
# PLACEHOLDER VIEWS (We'll build these step by step)
# ============================================================================

# We'll add these views as we progress:
# - Student registration view
# - Module registration/unregistration views
# - My Registrations view
# - Course-specific module list view