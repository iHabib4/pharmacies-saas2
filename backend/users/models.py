# apps/users/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ("customer", "Customer"),
        ("pharmacy", "Pharmacy"),
        ("rider", "Rider"),
        ("supplier", "Supplier"),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="customer",
        help_text="Role of the user in the system",
    )

    mobile_number = models.CharField(
        max_length=15,
        unique=True,
        null=True,
        blank=True,
        help_text="Mobile number for receiving payments (e.g., +254700000000)",
    )

    def __str__(self):
        return f"{self.username} ({self.role})"
