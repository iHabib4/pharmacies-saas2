from django.shortcuts import render

from .services import expiring_soon_batches


def pharmacy_dashboard(request):
    # Get batches expiring in next 30 days
    warnings = expiring_soon_batches(30)
    return render(request, "pharmacy/dashboard.html", {"warnings": warnings})
