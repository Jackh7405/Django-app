from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, Group
from django.urls import reverse

# ============================================================================
# MODULE MODEL - For Module Registration System
# ============================================================================
class Module(models.Model):
    """
    Represents a university module/course that students can register for.
    """
    
    # Category choices for modules
    CATEGORY_CHOICES = [
        ('CORE', 'Core Module'),
        ('OPTIONAL', 'Optional Module'),
        ('ELECTIVE', 'Elective Module'),
    ]
    
    # Basic module information
    name = models.CharField(max_length=200, help_text="Full name of the module")
    code = models.CharField(
        max_length=20, 
        unique=True,  # IMPORTANT: This makes the code unique for use in URLs
        help_text="Unique module code (e.g., 55-123456)"
    )
    credit = models.IntegerField(
        default=20,
        help_text="Credit hours for this module"
    )
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='CORE',
        help_text="Category of the module"
    )
    description = models.TextField(
        help_text="Detailed description of the module"
    )
    
    # Availability for registration
    availability = models.BooleanField(
        default=True,
        help_text="Is this module open for student registration?"
    )
    
    # Many-to-Many relationship with Groups (Groups represent Courses)
    courses_allowed = models.ManyToManyField(
        Group,
        related_name='modules',
        help_text="Which courses (Groups) are allowed to register for this module"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['code']  # Order modules by code
        verbose_name = 'Module'
        verbose_name_plural = 'Modules'
    
    def __str__(self):
        """Returns meaningful text representation"""
        return f"{self.code} - {self.name}"
    
    def get_absolute_url(self):
        """Returns the URL to access a particular module using its code (not ID)"""
        # We'll use the code in the URL instead of pk
        return reverse('itreporting:module-detail', kwargs={'code': self.code})
    
    def is_open_for_registration(self):
        """Helper method to check if module is available"""
        return self.availability
    
    def get_registered_students_count(self):
        """Returns count of students registered for this module"""
        return self.registrations.count()


# ============================================================================
# KEEP YOUR EXISTING ISSUE MODEL (for reference/backward compatibility)
# ============================================================================
#class Issue(models.Model):
#    """
#    Original IT Issue model - keeping for reference
#    You can delete this later if not needed
#    """
#    type = models.CharField(max_length=100, choices=[('Hardware', 'Hardware'), ('Software', 'Software')])
#    room = models.CharField(max_length=100)
#    urgent = models.BooleanField(default=False)
#    details = models.TextField()
#    date_submitted = models.DateTimeField(default=timezone.now)
#    description = models.TextField()
#    author = models.ForeignKey(User, related_name='issues', on_delete=models.CASCADE)
    
#    def __str__(self):
#        return f'{self.type} Issue in {self.room}'
    
#    def get_absolute_url(self):
#        return reverse('itreporting:issue-detail', kwargs={'pk': self.pk})Q
