# apps/payments/views.py

import uuid
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.orders.models import Order
from apps.payments.models import Payment


# -------------------------------
# CALLBACK (REAL USE LATER)
# -------------------------------
def mobile_money_callback(request):
    return HttpResponse("Callback received")


# -------------------------------
# INITIATE PAYMENT
# -------------------------------
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def mobile_money_payment(request):

    data = request.data
    order_id = data.get("order_id")
    phone_number = data.get("phone_number")
    provider = data.get("provider")  # TIGO / MPESA / YAS

    if not order_id or not phone_number or not provider:
        return Response(
            {"error": "order_id, phone_number, provider required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        order = Order.objects.get(id=order_id, consumer=request.user)
    except Order.DoesNotExist:
        return Response(
            {"error": "Order not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    # Create Payment record (IMPORTANT)
    payment = Payment.objects.create(
        order=order,
        amount=order.total_price,
        method=provider,
        status="PENDING",
        transaction_id=str(uuid.uuid4()),
    )

    # -------------------------------------------------
    # MOCK RESPONSE (replace with real Tigo API later)
    # -------------------------------------------------
    return Response(
        {
            "message": "Payment initiated",
            "payment_id": payment.id,
            "transaction_id": payment.transaction_id,
            "status": payment.status,
        },
        status=status.HTTP_200_OK,
    )
