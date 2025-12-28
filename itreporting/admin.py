from django.contrib import admin
from .models import Module

# ============================================================================
# MODULE ADMIN CONFIGURATION
# ============================================================================
@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    """
    Admin interface for Module model with enhanced display and filters
    """
    list_display = ['code', 'name', 'credit', 'category', 'availability', 'get_courses_display']
    list_filter = ['category', 'availability', 'courses_allowed']
    search_fields = ['code', 'name', 'description']
    filter_horizontal = ['courses_allowed']  # Better UI for many-to-many fields
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('code', 'name', 'credit', 'category')
        }),
        ('Details', {
            'fields': ('description', 'availability')
        }),
        ('Course Access', {
            'fields': ('courses_allowed',),
            'description': 'Select which courses (Groups) can register for this module'
        }),
    )
    
    def get_courses_display(self, obj):
        """Display list of courses allowed for this module"""
        courses = obj.courses_allowed.all()
        if courses:
            return ", ".join([course.name for course in courses])
        return "No courses assigned"
    get_courses_display.short_description = 'Allowed Courses'