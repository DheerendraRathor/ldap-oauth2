from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import InstituteAddress, Program, ContactNumber, SecondaryEmail, SentMessage


class InstituteAddressAdmin(SimpleHistoryAdmin):
    list_display = ['id', 'user', 'hostel', 'room']
    list_filter = ['hostel']
    search_fields = ['user__username', 'room']


class ProgramAdmin(SimpleHistoryAdmin):
    list_display = ['id', 'user', 'department', 'join_year', 'graduation_year', 'degree']
    list_filter = ['department', 'join_year', 'graduation_year', 'degree', ]
    search_fields = ['user__username', 'user__first_name', ]

    class Media:
        js = ['admin/js/list_filter_collapse.js', ]


class ContactNumberAdmin(SimpleHistoryAdmin):
    list_display = ['id', 'user', 'number']
    search_fields = ['user__username', 'user__first_name', 'number', ]


class SecondaryEmailAdmin(SimpleHistoryAdmin):
    list_display = ['id', 'user', 'email']
    search_fields = ['user__username', 'user__first_name', 'email', ]


class SentMessageAdmin(SimpleHistoryAdmin):
    list_display = ['id', 'message_id', 'sender', 'status', 'error_message', 'created', ]
    list_filter = ['status']
    search_fields = ['sender', 'user', ]


admin.site.register(InstituteAddress, InstituteAddressAdmin)
admin.site.register(Program, ProgramAdmin)
admin.site.register(ContactNumber, ContactNumberAdmin)
admin.site.register(SecondaryEmail, SecondaryEmailAdmin)
admin.site.register(SentMessage, SentMessageAdmin)
