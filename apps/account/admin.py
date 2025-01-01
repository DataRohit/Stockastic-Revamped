# Imports
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

# Get the User model
User = get_user_model()


# Register the User model
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """User Admin

    This class is used to customize the User admin

    Attributes:
        list_display (list): The fields to display in the list
        list_display_links (list): The fields to link in the list
        search_fields (list): The fields to search in the list
        ordering (list): The default ordering for the list
        fieldsets (tuple): The fieldsets to display in the form
        add_fieldsets (tuple): The fieldsets to display in the add form
    """

    # Attributes
    list_display = [
        "email",
        "first_name",
        "last_name",
        "username",
        "is_active",
        "is_superuser",
    ]
    list_display_links = ["email", "username"]
    search_fields = ["email", "username", "first_name", "last_name"]
    ordering = ["-date_joined"]
    fieldsets = (
        (_("Login Credentials"), {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("username", "first_name", "last_name")}),
        (_("Profile"), {"fields": ("avatar",)}),
        (
            _("Permissions and Groups"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important Dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
