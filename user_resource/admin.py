from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import InstituteAddress, Program, ContactNumber, SecondaryEmail, SentMessage


class InstituteAddressAdmin(SimpleHistoryAdmin):
    list_display = ['id', 'user', 'hostel', 'room']


class ProgramAdmin(SimpleHistoryAdmin):
    list_display = ['id', 'user', 'department', 'join_year', 'graduation_year', 'degree']


class ContactNumberAdmin(SimpleHistoryAdmin):
    list_display = ['id', 'user', 'number']


class SecondaryEmailAdmin(SimpleHistoryAdmin):
    list_display = ['id', 'user', 'email']


class SentMessageAdmin(SimpleHistoryAdmin):
    list_display = ['id', 'message_id', 'sender', 'status', 'error_message']


admin.site.register(InstituteAddress, InstituteAddressAdmin)
admin.site.register(Program, ProgramAdmin)
admin.site.register(ContactNumber, ContactNumberAdmin)
admin.site.register(SecondaryEmail, SecondaryEmailAdmin)
admin.site.register(SentMessage, SentMessageAdmin)
