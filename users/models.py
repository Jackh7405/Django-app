from django.contrib.auth.models import User, Group
from django.db import models

class Student(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        related_name='student',
        help_text="Linked user account"
    )
    
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
    
    photo = models.ImageField(
        default='student_photos/default.png',
        upload_to='student_photos',
        help_text="Student photo"
    )
    
    course = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='students',
        help_text="The course this student is enrolled in"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['user__last_name', 'user__first_name']
        verbose_name = 'Student'
        verbose_name_plural = 'Students'
    
    def __str__(self):
        if self.user.first_name and self.user.last_name:
            return f"{self.user.first_name} {self.user.last_name}"
        return self.user.username
    
    def get_full_name(self):
        return f"{self.user.first_name} {self.user.last_name}".strip() or self.user.username
    
    def get_registered_modules(self):
        return self.registrations.all()