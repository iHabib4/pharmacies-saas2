# apps/users/admin.py

from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()  # ✅ safe import of custom user model


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "last_name", "is_staff", "is_active")
    search_fields = ("email", "first_name", "last_name")
