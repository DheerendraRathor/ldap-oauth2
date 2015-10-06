from django.contrib import admin
from .models import InstituteAddress, Program, ContactNumber, SecondaryEmail, SentMessage


class InstituteAddressAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'hostel', 'room']


class ProgramAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'department', 'join_year', 'graduation_year', 'degree']


class ContactNumberAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'number']


class SecondaryEmailAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'email']


class SentMessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'message_id', 'status', 'error_message']


admin.site.register(InstituteAddress, InstituteAddressAdmin)
admin.site.register(Program, ProgramAdmin)
admin.site.register(ContactNumber, ContactNumberAdmin)
admin.site.register(SecondaryEmail, SecondaryEmailAdmin)
admin.site.register(SentMessage, SentMessageAdmin)
