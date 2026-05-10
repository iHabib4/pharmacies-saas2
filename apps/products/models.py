# apps/products/models.py

from django.db import models
from django.db.models import Sum

from apps.pharmacies.models import Pharmacy


# =========================
# PRODUCT
# =========================
class Product(models.Model):
    name = models.CharField(
        max_length=255,
    )

    description = models.TextField(
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    # =========================
    # TOTAL STOCK
    # =========================
    def total_stock(self, pharmacy=None):
        batches = self.batches.all()

        if pharmacy:
            batches = batches.filter(
                pharmacy=pharmacy
            )

        result = batches.aggregate(
            total=Sum("quantity")
        )

        return result["total"] or 0


# =========================
# MEDICINE BATCH
# =========================
class MedicineBatch(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="batches",
    )

    pharmacy = models.ForeignKey(
        Pharmacy,
        on_delete=models.CASCADE,
        related_name="batches",
    )

    batch_number = models.CharField(
        max_length=100,
    )

    quantity = models.PositiveIntegerField(
        default=0,
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-created_at"]

        unique_together = (
            "pharmacy",
            "batch_number",
        )

    def __str__(self):
        return (
            f"{self.product.name} | "
            f"{self.pharmacy.name} | "
            f"{self.batch_number}"
        )

    # =========================
    # REDUCE STOCK
    # =========================
    def reduce_stock(self, amount):
        if amount <= 0:
            raise ValueError(
                "Amount must be greater than zero."
            )

        if amount > self.quantity:
            raise ValueError(
                f"Cannot reduce stock by {amount}. "
                f"Only {self.quantity} available."
            )

        self.quantity -= amount
        self.save()

    # =========================
    # ADD STOCK
    # =========================
    def add_stock(self, amount):
        if amount <= 0:
            raise ValueError(
                "Amount must be greater than zero."
            )

        self.quantity += amount
        self.save()
