from django.contrib import admin
from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'roll_number', 'type']


admin.site.register(UserProfile, UserProfileAdmin)
