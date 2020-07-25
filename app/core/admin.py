from django.contrib import admin  # noqa
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin  # noqa
from django.utils.translation import gettext as _  # noqa

from core.models import (User, Tag, Ingredient, Recipe)  # noqa


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        (_("Personal Info"), {'fields': ('name',)}),
        (_("Permissions"), {'fields': ('is_active', 'is_staff',
                                       'is_superuser',)}),
        (_("Important dates"), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2',)
        }),
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    pass


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    pass
