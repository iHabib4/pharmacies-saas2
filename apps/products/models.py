from django.db import models
from django.db.models import Sum
from apps.pharmacies.models import Pharmacy


# =========================
# PRODUCT
# =========================
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    def total_stock(self, pharmacy=None):
        qs = self.batches.all()

        if pharmacy:
            qs = qs.filter(pharmacy=pharmacy)

        return qs.aggregate(total=Sum("quantity"))["total"] or 0


# =========================
# MEDICINE BATCH
# =========================
class MedicineBatch(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="batches"
    )

    pharmacy = models.ForeignKey(
        Pharmacy,
        on_delete=models.CASCADE,
        related_name="batches"
    )

    batch_number = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    # ✅ FIX: this was missing
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.pharmacy.name} - {self.batch_number}"

    def reduce_stock(self, amount):
        if amount > self.quantity:
            raise ValueError(
                f"Cannot reduce stock by {amount}. Only {self.quantity} available."
            )

        self.quantity -= amount
        self.save()
