from django.contrib.auth.models import User, Group
from django.db import models

# ============================================================================
# STUDENT MODEL - For Module Registration System
# ============================================================================
class Student(models.Model):
    """
    Extended user profile for students with all required information
    This replaces the old Profile model
    """
    
    # Link to Django User model (one-to-one relationship)
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        related_name='student',
        help_text="Linked user account"
    )
    
    # Personal Information
    date_of_birth = models.DateField(
        null=True,
        blank=True,
        help_text="Student's date of birth"
    )
    
    address = models.TextField(
        max_length=255,
        blank=True,
        help_text="Full address"
    )
    
    city = models.CharField(
        max_length=100,
        blank=True,
        help_text="City or town"
    )
    
    country = models.CharField(
        max_length=100,
        blank=True,
        default='United Kingdom',
        help_text="Country"
    )
    
    # Photo
    photo = models.ImageField(
        default='student_photos/default.png',
        upload_to='student_photos',
        help_text="Student photo"
    )
    
    # Course - Student enrolled in ONE course (Group)
    course = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students',
        help_text="The course this student is enrolled in"
    )
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['user__last_name', 'user__first_name']
        verbose_name = 'Student'
        verbose_name_plural = 'Students'
    
    def __str__(self):
        """Returns student name"""
        if self.user.first_name and self.user.last_name:
            return f"{self.user.first_name} {self.user.last_name}"
        return self.user.username
    
    def get_full_name(self):
        """Helper method to get full name"""
        return f"{self.user.first_name} {self.user.last_name}".strip() or self.user.username
    
    def get_registered_modules(self):
        """Returns all modules this student is registered for"""
        # We'll implement this when we create the Registration model
        return self.registrations.all()