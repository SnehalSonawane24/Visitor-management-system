from django.contrib import admin

# Register your models here.

from django.contrib.auth.admin import UserAdmin
from .models import UserAccount


class CustomUserAdmin(UserAdmin):
    model = UserAccount
    list_display = ("email", "name", "is_staff","is_manager", "is_superuser")
    list_filter = ("is_staff","is_manager", "is_superuser", "is_active")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("name",)}),
        ("Permissions", {"fields": ("is_active", "is_staff","is_manager", "is_superuser")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "name",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_manager",
                    "is_superuser",
                ),
            },
        ),
    )
    search_fields = ("email", "name")
    ordering = ("email",)


admin.site.register(UserAccount, CustomUserAdmin)
