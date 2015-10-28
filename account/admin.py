from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import UserProfile


class UserProfileAdmin(SimpleHistoryAdmin):
    list_display = ['id', 'user', 'roll_number', 'sex', 'type']
    list_filter = ['sex', 'type', ]
    search_fields = ['user__username', 'user__first_name', 'roll_number']


admin.site.register(UserProfile, UserProfileAdmin)
