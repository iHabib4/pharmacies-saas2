# apps/pharmacies/views.py
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.pharmacies.models import Rider

from .dispatch import find_best_rider
from .models import Pharmacy  # only import Pharmacy
from .serializers import PharmacySerializer
from .services import calculate_fastest_route


class PharmacyViewSet(viewsets.ModelViewSet):
    queryset = Pharmacy.objects.all()
    serializer_class = PharmacySerializer


def recommend_products_view(request):
    # Only active pharmacies
    all_pharmacies = Pharmacy.objects.filter(is_active=True)

    # Filter OTC products
    recommended_products = all_pharmacies.filter(is_otc=True)

    # Count prescription-only products
    excluded_count = all_pharmacies.filter(is_otc=False).count()

    context = {
        "recommended_products": recommended_products,
        "excluded_count": excluded_count,
        "warning_message": "⚠ Consult a doctor if symptoms persist.",
    }

    return render(request, "products/recommendations.html", context)


def assign_rider(delivery):
    rider = find_best_rider(delivery.pharmacy.latitude, delivery.pharmacy.longitude)

    if rider:
        delivery.rider = rider
        delivery.status = "assigned"

        # Route optimization
        route_info = calculate_fastest_route(
            (delivery.pharmacy.latitude, delivery.pharmacy.longitude),
            (delivery.customer.latitude, delivery.customer.longitude),
        )
        delivery.estimated_distance_km = route_info["distance_km"]
        delivery.estimated_time_min = route_info["traffic_duration_min"]

        rider.is_available = False
        rider.save()
        delivery.save()


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def update_location(request):
    """
    Riders send current location every 5 seconds.
    """
    user = request.user
    try:
        rider = Rider.objects.get(user=user)
    except Rider.DoesNotExist:
        return Response({"error": "Rider not found"}, status=404)

    latitude = request.data.get("latitude")
    longitude = request.data.get("longitude")

    if latitude is None or longitude is None:
        return Response({"error": "Missing latitude or longitude"}, status=400)

    rider.latitude = latitude
    rider.longitude = longitude
    rider.save()

    return Response({"status": "location updated"})
