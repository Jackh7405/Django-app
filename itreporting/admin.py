from django.contrib import admin
from .models import Module, Registration

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    """
    Admin interface for Module model with enhanced display and filters
    """
    list_display = ['code', 'name', 'credit', 'category', 'availability', 'get_courses_display', 'get_registration_count']
    list_filter = ['category', 'availability', 'courses_allowed']
    search_fields = ['code', 'name', 'description']
    filter_horizontal = ['courses_allowed']
    
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
    
    def get_registration_count(self, obj):
        """Display number of students registered"""
        return obj.get_registered_students_count()
    get_registration_count.short_description = 'Registrations'


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    """
    Admin interface for Registration model
    """
    list_display = ['get_student_name', 'get_module_code', 'get_module_name', 'date_registered']
    list_filter = ['date_registered', 'module__category', 'module']
    search_fields = [
        'student__user__username', 
        'student__user__first_name', 
        'student__user__last_name',
        'module__code',
        'module__name'
    ]
    date_hierarchy = 'date_registered'
    
    fieldsets = (
        ('Registration Details', {
            'fields': ('student', 'module')
        }),
    )
    
    readonly_fields = ['date_registered']
    
    def get_student_name(self, obj):
        """Display student name"""
        return obj.student.get_full_name()
    get_student_name.short_description = 'Student'
    
    def get_module_code(self, obj):
        """Display module code"""
        return obj.module.code
    get_module_code.short_description = 'Module Code'
    
    def get_module_name(self, obj):
        """Display module name"""
        return obj.module.name
    get_module_name.short_description = 'Module Name'