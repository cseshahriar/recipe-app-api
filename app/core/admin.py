from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from core.models import (
    User,
    Recipe,
    Tag,
    Ingredient
)


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


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'time_minutes', 'price', 'tags')
    search_fields = ('title', 'description')
    list_filter = ('user',)
    ordering = ('title',)

    def tags(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all])


class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'user', )
    search_fields = ('name', )
    list_filter = ('name', )
    ordering = ('-pk', )


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'user', )
    search_fields = ('name', )
    list_filter = ('name', )
    ordering = ('-pk', )


admin.site.register(User, CustomUserAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
