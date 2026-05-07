# apps/deliveries/views.py

from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.orders.models import Order
from apps.pharmacies.dispatch import find_best_rider
from apps.services import distribute_funds

from .models import Delivery, Payment
from .payment_services import initiate_mobile_payment
from .serializers import DeliverySerializer, OrderSerializer
from .services import find_nearest_riders


# ==================
# CONFIRM DELIVERY
# ==================
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def confirm_delivery(request, delivery_id):
    delivery = get_object_or_404(Delivery, id=delivery_id)
    delivery.status = "delivered"
    delivery.save()

    order = delivery.order

    if order.is_paid and not order.is_settled:
        distribute_funds(order)

    return Response({"message": "Delivery confirmed and funds distributed"})


# ==========================================
# ORDER VIEWSET
# ==========================================
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        order = serializer.save()

        # Create delivery automatically
        Delivery.objects.create(
            order=order,
            customer=order.consumer,
            pharmacy=order.pharmacy,
            status="pending",
        )


# ==========================================
# DELIVERY TRACKING
# ==========================================
class DeliveryTrackingViewSet(viewsets.ModelViewSet):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer

    @action(detail=True, methods=["get"])
    def track(self, request, pk=None):
        delivery = self.get_object()
        return Response(
            {
                "order": delivery.order.id,
                "rider": delivery.rider.id if delivery.rider else None,
                "status": delivery.status,
            }
        )


# ==========================================
# ASSIGN RIDER (AUTO)
# ==========================================
def assign_rider(delivery):
    lat = delivery.pharmacy.latitude
    lon = delivery.pharmacy.longitude

    rider = find_best_rider(lat, lon)  # ✅ FIXED INDENTATION

    if rider:
        delivery.rider = rider
        delivery.status = "assigned"
        rider.is_available = False
        rider.save()
        delivery.save()


# ==========================================
# AVAILABLE DELIVERIES
# ==========================================
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def available_deliveries(request):
    deliveries = Delivery.objects.filter(status="pending")
    serializer = DeliverySerializer(deliveries, many=True)
    return Response(serializer.data)


# ==========================================
# ACCEPT DELIVERY
# ==========================================
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def accept_delivery(request, delivery_id):
    if not hasattr(request.user, "rider"):
        return Response({"error": "Not a rider"}, status=403)

    rider = request.user.rider
    delivery = get_object_or_404(Delivery, id=delivery_id)

    if delivery.rider is not None:
        return Response({"error": "Delivery already assigned"}, status=400)

    delivery.rider = rider
    delivery.status = "assigned"

    rider.is_available = False
    rider.save()
    delivery.save()

    return Response(
        {
            "message": "Delivery accepted successfully",
            "delivery_id": delivery.id,
            "rider": rider.user.username,
        }
    )


# ==========================================
# UPDATE DELIVERY STATUS (with GPS)
# ==========================================
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def update_delivery_status(request, delivery_id):
    if not hasattr(request.user, "rider"):
        return Response({"error": "Not a rider"}, status=403)

    rider = request.user.rider
    delivery = get_object_or_404(Delivery, id=delivery_id)

    if delivery.rider != rider:
        return Response({"error": "Not your delivery"}, status=403)

    # Update GPS
    lat = request.data.get("latitude")
    lon = request.data.get("longitude")

    if lat is not None and lon is not None:
        delivery.latitude = lat
        delivery.longitude = lon

    # Status flow
    new_status = request.data.get("status")

    allowed_flow = {
        "assigned": ["picked"],
        "picked": ["on_the_way"],
        "on_the_way": ["delivered"],
    }

    current_status = delivery.status

    if new_status:
        if (
            current_status not in allowed_flow
            or new_status not in allowed_flow[current_status]
        ):
            return Response(
                {
                    "error": f"Invalid status transition from {current_status} to {new_status}"
                },
                status=400,
            )

        delivery.status = new_status

        # When delivered
        if new_status == "delivered":
            rider.is_available = True
            rider.total_deliveries += 1
            rider.save()

            order = delivery.order
            order.status = "delivered"

            if order.is_paid and not order.is_settled:
                distribute_funds(order)

            order.save()

    delivery.save()

    return Response(
        {
            "message": "Delivery updated",
            "delivery_id": delivery.id,
            "status": delivery.status,
            "latitude": delivery.latitude,
            "longitude": delivery.longitude,
        }
    )
