# pharmacy/services.py
from datetime import date, timedelta

from .models import MedicineBatch


def admin_dashboard_stats():
    today = date.today()
    warning_date = today + timedelta(days=30)  # expiring soon threshold

    total_medicines = MedicineBatch.objects.count()
    expired_medicines = MedicineBatch.objects.filter(expiry_date__lt=today).count()
    low_stock_medicines = MedicineBatch.objects.filter(
        quantity__lte=10
    ).count()  # threshold for low stock
    expiring_soon = MedicineBatch.objects.filter(
        expiry_date__lte=warning_date, expiry_date__gte=today
    ).count()

    return {
        "total_medicines": total_medicines,
        "expired_medicines": expired_medicines,
        "low_stock_medicines": low_stock_medicines,
        "expiring_soon": expiring_soon,
    }
