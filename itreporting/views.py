from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Module, Registration
from users.models import Student
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import DeleteView
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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
    """Contact Us page with form handling and email sending"""
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Validate form data
        if not all([name, email, subject, message]):
            messages.error(request, 'Please fill in all required fields.')
            return redirect('itreporting:contact')
        
        try:
            # Prepare email content
            email_subject = f'Contact Form: {subject}'
            email_message = f"""
New contact form submission from Sheffield Hallam Module Registration System

From: {name}
Email: {email}
Subject: {subject}

Message:
{message}

---
This email was sent from the Module Registration System contact form.
Reply directly to: {email}
            """
            
            # Send email
            from django.core.mail import send_mail
            from django.conf import settings
            
            send_mail(
                subject=email_subject,
                message=email_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_EMAIL],
                fail_silently=False,  # Raise exception if sending fails
            )
            
            messages.success(
                request, 
                f'Thank you {name}! Your message has been sent successfully. We will respond to {email} shortly.'
            )
            
        except Exception as e:
            # If email sending fails, show error but don't crash
            messages.error(
                request,
                f'Sorry, there was an error sending your message. Please try again later or email us directly at itservices@shu.ac.uk'
            )
            print(f"Email sending error: {e}")  # Log the error
        
        return redirect('itreporting:contact')
    
    return render(request, 'itreporting/contact.html', {'title': 'Contact Us'})


# ============================================================================
# MODULE VIEWS
# ============================================================================

class ModuleListView(ListView):
    """
    Display list of all modules
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
    slug_field = 'code'
    slug_url_kwarg = 'code'
    
    def get_context_data(self, **kwargs):
        """Add extra context for the template"""
        context = super().get_context_data(**kwargs)
        
        # Get all registrations for this module
        context['registrations'] = Registration.objects.filter(
            module=self.object
        ).select_related('student__user')
        
        # Check if current user is registered
        if self.request.user.is_authenticated:
            try:
                student = self.request.user.student
                context['is_registered'] = Registration.objects.filter(
                    student=student,
                    module=self.object
                ).exists()
            except Student.DoesNotExist:
                context['is_registered'] = False
        else:
            context['is_registered'] = False
        
        return context


# ============================================================================
# REGISTRATION VIEWS
# ============================================================================

@login_required
def register_module(request, code):
    """
    Register a student for a module
    """
    # Get the module
    module = get_object_or_404(Module, code=code)
    
    # Get the student
    try:
        student = request.user.student
    except Student.DoesNotExist:
        messages.error(request, 'You need to complete your student profile first.')
        return redirect('profile')
    
    # Check if module is open for registration
    if not module.availability:
        messages.error(request, f'{module.code} is currently closed for registration.')
        return redirect('itreporting:module-detail', code=code)
    
    # Check if student's course is allowed to register
    if student.course and student.course not in module.courses_allowed.all():
        messages.error(
            request, 
            f'Your course ({student.course.name}) is not allowed to register for {module.code}.'
        )
        return redirect('itreporting:module-detail', code=code)
    
    # Try to create registration
    registration, created = Registration.objects.get_or_create(
        student=student,
        module=module
    )
    
    if created:
        messages.success(
            request, 
            f'Successfully registered for {module.code} - {module.name}!'
        )
    else:
        messages.info(request, f'You are already registered for {module.code}.')
    
    return redirect('itreporting:module-detail', code=code)


@login_required
def unregister_module(request, code):
    """
    Unregister a student from a module
    """
    # Get the module
    module = get_object_or_404(Module, code=code)
    
    # Get the student
    try:
        student = request.user.student
    except Student.DoesNotExist:
        messages.error(request, 'Student profile not found.')
        return redirect('profile')
    
    # Try to find and delete the registration
    try:
        registration = Registration.objects.get(
            student=student,
            module=module
        )
        registration.delete()
        messages.success(
            request, 
            f'Successfully unregistered from {module.code} - {module.name}.'
        )
    except Registration.DoesNotExist:
        messages.error(request, f'You are not registered for {module.code}.')
    
    return redirect('itreporting:module-detail', code=code)


@login_required
def my_registrations(request):
    """
    Display all modules the current student is registered for
    """
    try:
        student = request.user.student
        registrations = Registration.objects.filter(
            student=student
        ).select_related('module').order_by('-date_registered')
        
        context = {
            'title': 'My Registrations',
            'registrations': registrations,
            'student': student
        }
        return render(request, 'itreporting/my_registrations.html', context)
    
    except Student.DoesNotExist:
        messages.error(request, 'Please complete your student profile first.')
        return redirect('profile')