# apps/deliveries/models.py

from django.conf import settings
from django.db import models
from django.utils import timezone

from apps.orders.models import Order
from apps.pharmacies.models import Pharmacy
from apps.products.models import Product
from apps.riders.models import Rider

User = settings.AUTH_USER_MODEL


# =========================
# DELIVERY MODEL
# =========================
class Delivery(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("assigned", "Assigned"),
        ("picked", "Picked"),
        ("on_the_way", "On the way"),
        ("delivered", "Delivered"),
    ]

    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, related_name="delivery"
    )

    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    pharmacy = models.ForeignKey(
        Pharmacy, on_delete=models.CASCADE, null=True, blank=True
    )

    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, blank=True
    )

    rider = models.ForeignKey(Rider, on_delete=models.SET_NULL, null=True, blank=True)

    # GPS tracking
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="pending")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Delivery {self.id} - {self.status}"


# =========================
# PAYMENT MODEL
# =========================
class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)

    amount = models.DecimalField(max_digits=10, decimal_places=2)

    method = models.CharField(
        max_length=20,
        choices=[
            ("mpesa", "M-Pesa"),
            ("tigopesa", "Tigo Pesa"),
            ("airtelmoney", "Airtel Money"),
        ],
    )

    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("paid", "Paid"),
            ("failed", "Failed"),
        ],
        default="pending",
    )

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Payment {self.id} - {self.status}"
