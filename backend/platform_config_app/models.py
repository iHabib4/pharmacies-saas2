from django.db import models


class PlatformSettings(models.Model):
    COMMISSION_TYPE_CHOICES = [
        ("per_order", "Per Order"),
        ("per_pharmacy", "Per Pharmacy"),
        ("per_month", "Per Month"),
    ]

    commission_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=10,
        help_text="Commission rate in percentage (e.g., 10 = 10%)",
    )
    commission_type = models.CharField(
        max_length=20, choices=COMMISSION_TYPE_CHOICES, default="per_order"
    )

    def __str__(self):
        return f"Platform Settings ({self.commission_type} - {self.commission_rate}%)"
