# apps/pharmacies/views.py

from django.shortcuts import render
from django.utils import timezone

from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.products.models import MedicineBatch
from apps.pharmacies.models import Pharmacy, Rider
from apps.pharmacies.serializers import PharmacySerializer

from .dispatch import find_best_rider
from .services import calculate_fastest_route


# =========================
# PHARMACY CRUD API
# =========================

class PharmacyViewSet(viewsets.ModelViewSet):
    queryset = Pharmacy.objects.all()
    serializer_class = PharmacySerializer

    # ✅ FIX: automatically assign logged-in user as owner
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# =========================
# PRODUCT RECOMMENDATION (WEB)
# =========================

def recommend_products_view(request):
    pharmacies = Pharmacy.objects.filter(is_active=True)

    recommended_products = pharmacies.filter(is_otc=True)
    excluded_count = pharmacies.filter(is_otc=False).count()

    return render(request, "products/recommendations.html", {
        "recommended_products": recommended_products,
        "excluded_count": excluded_count,
        "warning_message": "⚠ Consult a doctor if symptoms persist.",
    })


# =========================
# RIDER ASSIGNMENT LOGIC
# =========================

def assign_rider(delivery):
    rider = find_best_rider(
        delivery.pharmacy.latitude,
        delivery.pharmacy.longitude
    )

    if not rider:
        return

    route = calculate_fastest_route(
        (delivery.pharmacy.latitude, delivery.pharmacy.longitude),
        (delivery.customer.latitude, delivery.customer.longitude),
    )

    delivery.rider = rider
    delivery.status = "assigned"
    delivery.estimated_distance_km = route.get("distance_km", 0)
    delivery.estimated_time_min = route.get("traffic_duration_min", 0)

    rider.is_available = False

    rider.save()
    delivery.save()


# =========================
# RIDER LOCATION UPDATE API
# =========================

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def update_location(request):
    try:
        rider = Rider.objects.get(user=request.user)
    except Rider.DoesNotExist:
        return Response({"error": "Rider not found"}, status=404)

    latitude = request.data.get("latitude")
    longitude = request.data.get("longitude")

    if latitude is None or longitude is None:
        return Response({"error": "Missing coordinates"}, status=400)

    rider.latitude = latitude
    rider.longitude = longitude
    rider.save()

    return Response({"status": "location updated"})


# =========================
# PHARMACY DASHBOARD STATS
# =========================

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def pharmacy_stats(request):
    user = request.user

    # safe check for linked pharmacy
    if not hasattr(user, "pharmacy") or not user.pharmacy:
        return Response({"error": "No pharmacy linked"}, status=400)

    pharmacy = user.pharmacy
    batches = MedicineBatch.objects.filter(pharmacy=pharmacy)

    today = timezone.now().date()
    low_stock_threshold = 5

    low_stock_count = batches.filter(quantity__lte=low_stock_threshold).count()
    expired_count = batches.filter(expiry_date__lt=today).count()

    return Response({
        "pharmacy_id": pharmacy.id,
        "total_batches": batches.count(),
        "low_stock": low_stock_count,
        "expired": expired_count,
    })
