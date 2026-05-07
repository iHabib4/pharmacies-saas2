from django.contrib import admin
from .models import Consumer


@admin.register(Consumer)
class ConsumerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "phone",
        "email",
        "created_at",
    )

    search_fields = (
        "first_name",
        "last_name",
        "phone",
        "email",
    )

    ordering = ("first_name",)
