from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, Group
from django.urls import reverse


from users.models import Student


class Module(models.Model):
    CATEGORY_CHOICES = [
        ('CORE', 'Core Module'),
        ('OPTIONAL', 'Optional Module'),
        ('ELECTIVE', 'Elective Module'),
    ]
    
    name = models.CharField(max_length=200, help_text="Full name of the module")
    code = models.CharField(
        max_length=20, 
        unique=True, 
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
    
    availability = models.BooleanField(
        default=True,
        help_text="Is this module open for student registration?"
    )
    
    courses_allowed = models.ManyToManyField(
        Group,
        related_name='modules',
        help_text="Which courses (Groups) are allowed to register for this module"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['code'] 
        verbose_name = 'Module'
        verbose_name_plural = 'Modules'
    
    def __str__(self):
        return f"{self.code} - {self.name}"
    
    def get_absolute_url(self):
        return reverse('itreporting:module-detail', kwargs={'code': self.code})
    
    def is_open_for_registration(self):
        return self.availability
    
    def get_registered_students_count(self):
        return self.registrations.count()
    
    def get_registered_students(self):
        return Student.objects.filter(registrations__module=self)


class Registration(models.Model):
    """
    Represents a student's registration to a module.
    This is the many-to-many relationship between Student and Module.
    """
    
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='registrations',
        help_text="The student who registered for this module"
    )
    
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name='registrations',
        help_text="The module being registered for"
    )
    
    date_registered = models.DateTimeField(
        auto_now_add=True,
        help_text="When the student registered for this module"
    )
    
    class Meta:
        unique_together = ['student', 'module']
        ordering = ['-date_registered'] 
        verbose_name = 'Registration'
        verbose_name_plural = 'Registrations'
    
    def __str__(self):
        return f"{self.student} registered for {self.module.code}"
    
    def get_student_name(self):
        return self.student.get_full_name()
    
    def get_module_name(self):
        return self.module.name