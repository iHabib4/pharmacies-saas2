# apps/payments/views.py

import random

from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.orders.models import Order


# -------------------------------
# Placeholder for mobile money callback
# -------------------------------
def mobile_money_callback(request):
    return HttpResponse("Callback received")


# -------------------------------
# Mobile Money Payment Endpoint
# -------------------------------
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def mobile_money_payment(request):
    """
    Endpoint to process mobile money payments for an order.
    Expects JSON with:
      - order_id: int
      - phone_number: str
      - provider: str (e.g., "Tigo Pesa", "M-Pesa")
    """
    data = request.data
    order_id = data.get("order_id")
    phone_number = data.get("phone_number")
    provider = data.get("provider")

    # Validate input
    if not order_id or not phone_number or not provider:
        return Response(
            {"error": "order_id, phone_number, and provider are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Check if the order exists and belongs to the logged-in user
    try:
        order = Order.objects.get(id=order_id, consumer=request.user)
    except Order.DoesNotExist:
        return Response(
            {"error": "Order not found or does not belong to this user"},
            status=status.HTTP_404_NOT_FOUND,
        )

    # Simulate payment process (replace with real provider API later)
    payment_success = random.choice([True, False])

    if payment_success:
        order.payment_status = "paid"
        order.payment_provider = provider
        order.status = "pending"  # Order confirmed but not yet in transit
        order.save()
        return Response(
            {
                "message": f"Payment successful via {provider}",
                "order_id": order.id,
                "payment_status": order.payment_status,
            },
            status=status.HTTP_200_OK,
        )
    else:
        order.payment_status = "failed"
        order.save()
        return Response(
            {
                "message": f"Payment failed via {provider}",
                "order_id": order.id,
                "payment_status": order.payment_status,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
