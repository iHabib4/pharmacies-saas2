# pharmacy/views.py
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Pharmacy, Product
from .services import admin_dashboard_stats


@api_view(["GET"])
def admin_dashboard(request):
    stats = admin_dashboard_stats()
    return Response(stats)
    return render(request, "pharmacy/admin_dashboard.html", {"stats": stats})


def marketplace(request):
    pharmacies = Pharmacy.objects.all()
    return render(request, "pharmacy/marketplace.html", {"pharmacies": pharmacies})


def search_medicine(request):
    query = request.GET.get("q", "")
    products = Product.objects.filter(name__icontains=query)
    return render(request, "pharmacy/search_results.html", {"products": products})
