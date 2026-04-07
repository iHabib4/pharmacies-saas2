# apps/riders/models.py

from django.db import models

from apps.users.models import CustomUser


class Rider(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="rider_profile"
    )

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    is_available = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    vehicle_type = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    rating = models.FloatField(default=5.0)
    total_deliveries = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email
