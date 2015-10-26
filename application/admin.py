from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import Application


class ApplicationAdmin(SimpleHistoryAdmin):
    list_display = ['id', 'name', 'user', 'created_on', 'modified_on', 'is_anonymous', ]


admin.site.unregister(Application)
admin.site.register(Application, ApplicationAdmin)
