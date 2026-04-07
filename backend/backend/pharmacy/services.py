from datetime import date, timedelta

from .models import MedicineBatch


def expiring_soon_batches(days=30):
    """
    Returns batches that will expire in the next `days`.
    Default is 30 days.
    """
    warning_date = date.today() + timedelta(days=days)
    return MedicineBatch.objects.filter(expiry_date__lte=warning_date)
