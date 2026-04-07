# apps/orders/models.py

import random
from decimal import Decimal

from django.conf import settings
from django.db import models

from apps.pharmacies.models import Pharmacy
from apps.products.models import MedicineBatch, Product
from apps.riders.models import Rider
from platform_config_app.models import PlatformSettings


class Order(models.Model):
    consumer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        db_column="customer_id",
        related_name="orders",
    )

    pharmacy = models.ForeignKey(
        Pharmacy,
        on_delete=models.CASCADE,
        db_column="pharmacy_id",
        related_name="orders",
    )

    rider = models.ForeignKey(
        Rider,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column="rider_id",
        related_name="orders",
    )

    delivery_address = models.CharField(max_length=255, blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    commission = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    vendor_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("in_transit", "In Transit"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    ]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="pending")

    PAYMENT_STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("failed", "Failed"),
    ]
    payment_status = models.CharField(
        max_length=20, choices=PAYMENT_STATUS_CHOICES, default="pending"
    )
    payment_provider = models.CharField(max_length=50, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "orders_order"

    def save(self, *args, **kwargs):
        platform_settings = PlatformSettings.objects.first()
        commission_rate = (
            Decimal(platform_settings.commission_rate) / Decimal(100)
            if platform_settings and getattr(platform_settings, "commission_rate", None)
            else Decimal(0)
        )

        if self.total_price:
            self.total_price = Decimal(self.total_price)
            self.commission = self.total_price * commission_rate
            self.vendor_amount = self.total_price - self.commission

        super().save(*args, **kwargs)

    def __str__(self):
        consumer_name = self.consumer.first_name if self.consumer else "Unknown"
        return f"Order #{self.id} - {consumer_name} @ {self.pharmacy.name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    batch = models.ForeignKey(
        MedicineBatch, on_delete=models.CASCADE, null=True, blank=True
    )
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("in_transit", "In Transit"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    ]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="pending")

    payment_provider = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    estimated_distance_km = models.FloatField(null=True, blank=True)
    delivery_lat = models.FloatField(null=True, blank=True)
    delivery_lng = models.FloatField(null=True, blank=True)

    delivery_code = models.CharField(max_length=4, blank=True, null=True, unique=True)

    class Meta:
        db_table = "orders_orderitem"

    def generate_delivery_code(self):
        while True:
            code = f"{random.randint(1000, 9999)}"
            if not OrderItem.objects.filter(delivery_code=code).exists():
                self.delivery_code = code
                return code

    def save(self, *args, **kwargs):
        if not self.delivery_code:
            self.generate_delivery_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} x {self.quantity} (Order #{self.order.id})"
