from datetime import date

from .models import MedicineBatch


def disable_expired_medicines():

    expired_batches = MedicineBatch.objects.filter(expiry_date__lt=date.today())

    for batch in expired_batches:

        batch.quantity = 0
        batch.save()
