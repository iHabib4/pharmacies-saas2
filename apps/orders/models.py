# apps/orders/models.py

import random
from decimal import Decimal

from django.conf import settings
from django.db import models
from apps.pharmacies.models import Pharmacy
from apps.riders.models import Rider
from apps.products.models import Product


# =========================
# ORDER MODEL
# =========================
class Order(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("packed", "Packed"),
        ("in_transit", "In Transit"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    ]

    consumer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders",
        null=True,
        blank=True,
    )

    pharmacy = models.ForeignKey(
        Pharmacy,
        on_delete=models.CASCADE,
        related_name="orders",
    )

    rider = models.ForeignKey(
        Rider,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders",
    )

    delivery_address = models.CharField(max_length=255, null=True, blank=True)

    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    commission = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    vendor_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )

    payment_status = models.CharField(
        max_length=20,
        default="pending",
    )

    payment_provider = models.CharField(max_length=50, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "orders_order"

    def save(self, *args, **kwargs):
        platform_settings = None

        commission_rate = Decimal("0")

        if platform_settings and platform_settings.commission_rate:
            commission_rate = Decimal(platform_settings.commission_rate) / Decimal("100")

        self.total_price = Decimal(self.total_price or 0)
        self.commission = self.total_price * commission_rate
        self.vendor_amount = self.total_price - self.commission

        super().save(*args, **kwargs)

    def __str__(self):
        name = (
            self.consumer.mobile_number
            if self.consumer
            else "Customer"
        )
        return f"Order #{self.id} - {name}"


# =========================
# ORDER ITEM MODEL
# =========================
class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField(default=1)

    price = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(
        max_length=20,
        default="pending",
    )

    delivery_code = models.CharField(
        max_length=4,
        unique=True,
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "orders_orderitem"

    def generate_delivery_code(self):
        while True:
            code = str(random.randint(1000, 9999))
            if not OrderItem.objects.filter(delivery_code=code).exists():
                self.delivery_code = code
                return code

    def save(self, *args, **kwargs):
        if not self.delivery_code:
            self.generate_delivery_code()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product} x {self.quantity} (Order #{self.order.id})"
