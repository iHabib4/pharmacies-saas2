from django.db import models
from django.conf import settings


# -----------------------------
# Audit Log
# -----------------------------
class AuditLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    action = models.CharField(max_length=20)
    path = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} by {self.user}"


# -----------------------------
# Rider Location Tracking
# -----------------------------
class RiderLocation(models.Model):
    rider = models.ForeignKey(
        "riders.Rider",
        on_delete=models.CASCADE,
        related_name="locations"
    )
    latitude = models.FloatField()
    longitude = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.rider} @ {self.latitude}, {self.longitude}"
