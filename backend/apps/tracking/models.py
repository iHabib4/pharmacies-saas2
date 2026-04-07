# Create your models here.
from django.db import models

from apps.riders.models import Rider


class RiderLocation(models.Model):

    rider = models.ForeignKey(Rider, on_delete=models.CASCADE)

    latitude = models.FloatField()

    longitude = models.FloatField()

    updated_at = models.DateTimeField(auto_now=True)
