from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'user_username', 'course', 'city', 'country', 'date_of_birth']
    list_filter = ['course', 'country', 'city']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'user__email']
    
    fieldsets = (
        ('User Account', {
            'fields': ('user',)
        }),
        ('Personal Information', {
            'fields': ('date_of_birth', 'photo')
        }),
        ('Address', {
            'fields': ('address', 'city', 'country')
        }),
        ('Academic', {
            'fields': ('course',)
        }),
    )
    
    def get_full_name(self, obj):
        return obj.get_full_name()
    get_full_name.short_description = 'Name'
    
    def user_username(self, obj):

        return obj.user.username
    user_username.short_description = 'Username'