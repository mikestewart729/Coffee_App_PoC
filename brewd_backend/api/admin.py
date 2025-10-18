from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'location_lat', 'location_lng', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Location Settings', {'fields': ('location_lat', 'location_lng', 'default_search_radius')}),
    )
