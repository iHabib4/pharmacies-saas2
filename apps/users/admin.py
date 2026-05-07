# apps/users/admin.py

from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "get_mobile_number",
        "get_role",
        "is_staff",
        "is_active",
    )

    search_fields = (
        "mobile_number",
        "email",
    )

    list_filter = (
        "is_staff",
        "is_active",
    )

    ordering = ("-id",)

    readonly_fields = ("id",)

    def get_mobile_number(self, obj):
        return getattr(obj, "mobile_number", None)
    get_mobile_number.short_description = "Mobile Number"

    def get_role(self, obj):
        return getattr(obj, "role", None)
    get_role.short_description = "Role"
