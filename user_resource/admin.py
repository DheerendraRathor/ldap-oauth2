from django.contrib import admin
from .models import InstituteAddress, Program, ContactNumber, SecondaryEmail


class InstituteAddressAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'hostel', 'room']


class ProgramAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'department', 'join_year', 'graduation_year', 'degree']


class ContactNumberAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'number']


class SecondaryEmailAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'email']


admin.site.register(InstituteAddress, InstituteAddressAdmin)
admin.site.register(Program, ProgramAdmin)
admin.site.register(ContactNumber, ContactNumberAdmin)
admin.site.register(SecondaryEmail, SecondaryEmailAdmin)