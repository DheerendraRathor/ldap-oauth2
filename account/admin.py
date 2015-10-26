from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import UserProfile


class UserProfileAdmin(SimpleHistoryAdmin):
    list_display = ['id', 'user', 'roll_number', 'type']


admin.site.register(UserProfile, UserProfileAdmin)
