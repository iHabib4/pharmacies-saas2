from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    Adds role and mobile_number fields.
    """

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
        help_text="Designates the role of the user in the system.",
    )

    mobile_number = models.CharField(
        max_length=15,
        unique=True,
        null=True,
        blank=True,
        help_text="Optional mobile number for the user.",
    )

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["username"]

    def __str__(self):
        return f"{self.username} ({self.role})"


class Wallet(models.Model):
    """
    Wallet linked to each user.
    Stores the user's balance.
    """

    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="wallet"
    )
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.0)

    class Meta:
        verbose_name = "Wallet"
        verbose_name_plural = "Wallets"

    def __str__(self):
        return f"{self.user.username} Wallet: {self.balance}"
