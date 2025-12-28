from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Module, Registration
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import DeleteView
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User, Group
from django.contrib import messages

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
    """Contact Us page with form handling"""
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # For now, just show success message
        # We'll implement email sending in the Intermediate Requirements
        messages.success(
            request, 
            f'Thank you {name}! Your message has been received. We will respond to {email} shortly.'
        )
        return redirect('itreporting:contact')
    
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