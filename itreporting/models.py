from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, Group
from django.urls import reverse

# Import Student model from users app
from users.models import Student

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
        help_text="Unique module code (e.g., 55-606366)"
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
    
    def get_registered_students(self):
        """Returns all students registered for this module"""
        return Student.objects.filter(registrations__module=self)


# ============================================================================
# REGISTRATION MODEL - Links Students to Modules
# ============================================================================
class Registration(models.Model):
    """
    Represents a student's registration to a module.
    This is the many-to-many relationship between Student and Module.
    """
    
    # The student who registered
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='registrations',
        help_text="The student who registered for this module"
    )
    
    # The module being registered for
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name='registrations',
        help_text="The module being registered for"
    )
    
    # Date when registration occurred
    date_registered = models.DateTimeField(
        auto_now_add=True,
        help_text="When the student registered for this module"
    )
    
    class Meta:
        # Ensure a student can only register once per module
        unique_together = ['student', 'module']
        ordering = ['-date_registered']  # Most recent first
        verbose_name = 'Registration'
        verbose_name_plural = 'Registrations'
    
    def __str__(self):
        """Returns meaningful text representation"""
        return f"{self.student} registered for {self.module.code}"
    
    def get_student_name(self):
        """Helper method to get student name"""
        return self.student.get_full_name()
    
    def get_module_name(self):
        """Helper method to get module name"""
        return self.module.name