# apps/payments/models.py

from django.db import models
from apps.orders.models import Order


class Payment(models.Model):

    METHOD_CHOICES = (
        ("TIGO", "Tigo Pesa"),
        ("YAS", "Airtel Money (Yas)"),
        ("MPESA", "M-Pesa"),
        ("CASH", "Cash"),
    )

    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("COMPLETED", "Completed"),
        ("FAILED", "Failed"),
    )

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="payments"
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)

    method = models.CharField(
        max_length=20,
        choices=METHOD_CHOICES
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING"
    )

    transaction_id = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.id} - {self.status}"
