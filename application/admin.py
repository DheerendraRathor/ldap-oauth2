from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import Application


class ApplicationAdmin(SimpleHistoryAdmin):
    list_display = ['id', 'name', 'user', 'total_users', 'created_on', 'modified_on', 'is_anonymous']

    def total_users(self, obj):
        return obj.get_user_count()


admin.site.unregister(Application)
admin.site.register(Application, ApplicationAdmin)
