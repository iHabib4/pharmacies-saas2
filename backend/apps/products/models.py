# apps/products/models.py

from django.db import models
from django.db.models import Sum


class Pharmacy(models.Model):
    name = models.CharField(max_length=255)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    is_open = models.BooleanField(default=True)
    estimated_delivery_time = models.IntegerField(default=0)  # in minutes

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    def total_stock(self, pharmacy=None):
        """
        Returns total quantity of this product across all batches,
        optionally filtered by a specific pharmacy.
        """
        qs = self.batches.all()
        if pharmacy:
            qs = qs.filter(pharmacy=pharmacy)
        return qs.aggregate(total=Sum("quantity"))["total"] or 0


class MedicineBatch(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="batches"
    )
    pharmacy = models.ForeignKey(
        Pharmacy, on_delete=models.CASCADE, related_name="batches"
    )
    batch_number = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} - {self.pharmacy.name} - {self.batch_number}"

    def reduce_stock(self, amount):
        if amount > self.quantity:
            raise ValueError(
                f"Cannot reduce stock by {amount}. Only {self.quantity} available."
            )
        self.quantity -= amount
        self.save()
