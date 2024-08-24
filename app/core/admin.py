from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core.models import User
from django.utils.translation import gettext_lazy as _


class CustomUserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'name']  # Ensure 'name' is listed here
    fieldsets = (
        (None, {"fields": ('email', 'password')}),
        (
            _("Permissions"),
            {
                'fields': (
                    'is_active', 'is_staff', 'is_superuser'
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login', )}),
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields': (
                'email',
                'password1',
                'password2',
                'name',
                'is_active',
                'is_staff',
                'is_superuser'
            )
        }),
    )

    filter_horizontal = ()  # No filter_horizontal fields
    list_filter = ('is_active', 'is_staff', 'is_superuser')


admin.site.register(User, CustomUserAdmin)
