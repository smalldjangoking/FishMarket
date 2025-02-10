from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from .models import User, NovaAddresses


class NovaAddressesInline(admin.StackedInline):
    model = NovaAddresses
    extra = 0


class UserAdmin(BaseUserAdmin):
    inlines = (NovaAddressesInline,)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'name', 'last_name', 'phone_number', 'last_login')}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'password1', 'password2')
            }
        ),
    )

    list_display = ('email', 'name', 'last_name', 'phone_number')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email', 'phone_number', 'name', 'last_name')
    ordering = ('last_login',)
    filter_horizontal = ('groups', 'user_permissions',)




admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
