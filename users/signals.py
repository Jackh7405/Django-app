from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Student

@receiver(post_save, sender=User)
def create_student(sender, instance, created, **kwargs):
    """
    Automatically create a Student profile when a new User is created
    """
    if created:
        Student.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_student(sender, instance, **kwargs):
    """
    Save the Student profile when User is saved
    """
    # Only save if student profile exists
    if hasattr(instance, 'student'):
        instance.student.save()