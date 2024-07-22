from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from . import models
from django.utils.translation import gettext as _


class CustomUserAdmin(BaseUserAdmin):
    model = models.CustomUser
    ordering = ['id']
    list_display = ['id', 'username', 'is_staff', 'is_active']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (
            _('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
        (
            _('Important dates'), {'fields': ('last_login',)}
        )
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('username',)


admin.site.register(models.CustomUser, CustomUserAdmin)
admin.site.register(models.Books)
admin.site.register(models.Reviews)


