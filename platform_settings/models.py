from django.db import models


class PlatformSettings(models.Model):
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    commission_type = models.CharField(
        max_length=20,
        choices=[
            ("percentage", "Percentage"),
            ("fixed", "Fixed"),
        ],
        default="percentage"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Platform Setting"
        verbose_name_plural = "Platform Settings"

    def __str__(self):
        return f"{self.commission_rate} ({self.commission_type})"
