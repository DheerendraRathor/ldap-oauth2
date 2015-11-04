from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from simple_history.admin import SimpleHistoryAdmin

from user_resource.models import ContactNumber, InstituteAddress, Program, SecondaryEmail

from .models import UserProfile


class UserProfileAdmin(SimpleHistoryAdmin):
    list_display = ['id', 'user', 'roll_number', 'sex', 'type']
    list_filter = ['sex', 'type', ]
    search_fields = ['user__username', 'user__first_name', 'roll_number']


class InstituteAddressInline(admin.TabularInline):
    model = InstituteAddress


class UserProfileInline(admin.StackedInline):
    model = UserProfile


class ProgramInline(admin.StackedInline):
    model = Program


class ContactInline(admin.TabularInline):
    model = ContactNumber


class SecondaryEmailInline(admin.TabularInline):
    model = SecondaryEmail


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    readonly_fields = ('username', 'first_name', 'last_name', 'email', 'last_login', 'date_joined')

    inlines = [InstituteAddressInline, UserProfileInline, ProgramInline, ContactInline, SecondaryEmailInline]


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
