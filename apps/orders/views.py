# apps/orders/views.py

from decimal import Decimal
from datetime import timedelta

from django.db.models import Sum
from django.db.models.functions import TruncDate
from django.utils import timezone

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.orders.models import Order, OrderItem
from apps.deliveries.models import Delivery
from apps.pharmacies.models import Pharmacy
from apps.products.models import MedicineBatch, Product

from .serializers import OrderSerializer


# =========================================================
# 1️⃣ CREATE ORDER
# =========================================================
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_order_view(request):
    data = request.data

    items = data.get("items")
    delivery_address = data.get("delivery_address")
    pharmacy_id = data.get("pharmacy_id")

    if not items or not delivery_address or not pharmacy_id:
        return Response(
            {
                "error":
                "items, delivery_address, and pharmacy_id required"
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    # =========================
    # GET PHARMACY
    # =========================
    try:
        pharmacy = Pharmacy.objects.get(id=pharmacy_id)
    except Pharmacy.DoesNotExist:
        return Response(
            {"error": "Pharmacy not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    # =========================
    # CREATE ORDER
    # =========================
    order = Order.objects.create(
        consumer=request.user,
        pharmacy=pharmacy,
        delivery_address=delivery_address,
        total_price=Decimal("0.00"),
        status="pending",
    )

    total_price = Decimal("0.00")

    # =========================
    # PROCESS ITEMS
    # =========================
    for item in items:
        product_id = item.get("product_id")
        quantity = int(item.get("quantity", 1))

        if not product_id or quantity <= 0:
            return Response(
                {"error": "Invalid item"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(
                {"error": "Product not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # =========================
        # GET AVAILABLE BATCH
        # =========================
        batch = (
            MedicineBatch.objects.filter(
                product=product,
                pharmacy=pharmacy,
                quantity__gt=0,
            )
            .order_by("id")
            .first()
        )

        if not batch:
            return Response(
                {"error": f"{product.name} out of stock"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if batch.quantity < quantity:
            return Response(
                {
                    "error":
                    f"Only {batch.quantity} available"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # =========================
        # CALCULATE PRICE
        # =========================
        price = batch.price * quantity
        total_price += price

        # =========================
        # REDUCE STOCK
        # =========================
        batch.quantity -= quantity
        batch.save()

        # =========================
        # CREATE ORDER ITEM
        # =========================
        OrderItem.objects.create(
            order=order,
            product=product,
            batch=batch,
            quantity=quantity,
            price=price,
        )

    # =========================
    # SAVE TOTAL
    # =========================
    order.total_price = total_price
    order.save()

    # =========================
    # CREATE DELIVERY
    # =========================
    Delivery.objects.create(
        order=order,
        pharmacy=pharmacy,
        status="pending",
    )

    return Response(
        {
            "message": "Order created",
            "order_id": order.id,
            "total_price": float(total_price),
        },
        status=status.HTTP_201_CREATED,
    )


# =========================================================
# 2️⃣ ORDER ETA
# =========================================================
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_order_eta(request, order_id):
    try:
        order = Order.objects.get(
            id=order_id,
            consumer=request.user,
        )

        return Response({
            "order_id": order.id,
            "eta_minutes": 30,
        })

    except Order.DoesNotExist:
        return Response(
            {"error": "Order not found"},
            status=status.HTTP_404_NOT_FOUND,
        )


# =========================================================
# 3️⃣ RIDER PERFORMANCE
# =========================================================
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def rider_performance(request, rider_id):
    return Response({
        "rider_id": rider_id,
        "completed_orders": 50,
        "average_delivery_time": 28,
    })


# =========================================================
# 4️⃣ CONFIRM DELIVERY
# =========================================================
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def confirm_delivery(request, order_id):
    try:
        order = Order.objects.get(
            id=order_id,
            consumer=request.user,
        )

        if order.status == "completed":
            return Response({
                "message": "Already delivered"
            })

        order.status = "completed"
        order.save()

        return Response({
            "message": "Delivery confirmed"
        })

    except Order.DoesNotExist:
        return Response(
            {"error": "Order not found"},
            status=status.HTTP_404_NOT_FOUND,
        )


# =========================================================
# 5️⃣ PHARMACY REVENUE
# =========================================================
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def pharmacy_revenue_view(request):
    try:
        pharmacy = Pharmacy.objects.get(owner=request.user)

    except Pharmacy.DoesNotExist:
        return Response(
            {"error": "No pharmacy found"},
            status=status.HTTP_403_FORBIDDEN,
        )

    orders = Order.objects.filter(
        pharmacy=pharmacy,
        status="completed",
    )

    total_sales = (
        orders.aggregate(total=Sum("total_price"))["total"]
        or Decimal("0.00")
    )

    commission = total_sales * Decimal("0.10")

    return Response({
        "pharmacy_id": pharmacy.id,
        "pharmacy_name": pharmacy.name,
        "total_sales": float(total_sales),
        "commission": float(commission),
    })


# =========================================================
# 6️⃣ USER ORDERS
# =========================================================
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_orders(request):
    orders = (
        Order.objects.filter(
            consumer=request.user
        )
        .order_by("-created_at")
    )

    serializer = OrderSerializer(
        orders,
        many=True,
    )

    return Response(serializer.data)


# =========================================================
# 7️⃣ LIST ORDERS
# =========================================================
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_orders(request):
    user = request.user

    # =========================
    # PHARMACY OWNER
    # =========================
    if hasattr(user, "pharmacy"):
        orders = Order.objects.filter(
            pharmacy=user.pharmacy
        )

    # =========================
    # NORMAL USER
    # =========================
    else:
        orders = Order.objects.filter(
            consumer=user
        )

    serializer = OrderSerializer(
        orders.order_by("-created_at"),
        many=True,
    )

    return Response(serializer.data)


# =========================================================
# 8️⃣ EARNINGS ANALYTICS
# =========================================================
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def earnings_analytics(request):
    try:
        pharmacy = Pharmacy.objects.get(
            owner=request.user
        )

    except Pharmacy.DoesNotExist:
        return Response(
            {"error": "No pharmacy found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    completed_orders = Order.objects.filter(
        pharmacy=pharmacy,
        status="completed",
    )

    # =========================
    # TOTAL SALES
    # =========================
    total = (
        completed_orders.aggregate(
            total=Sum("total_price")
        )["total"]
        or Decimal("0.00")
    )

    # =========================
    # WEEKLY SALES
    # =========================
    week_ago = timezone.now() - timedelta(days=7)

    weekly = (
        completed_orders.filter(
            created_at__gte=week_ago
        )
        .aggregate(total=Sum("total_price"))["total"]
        or Decimal("0.00")
    )

    # =========================
    # MONTHLY SALES
    # =========================
    month_ago = timezone.now() - timedelta(days=30)

    monthly = (
        completed_orders.filter(
            created_at__gte=month_ago
        )
        .aggregate(total=Sum("total_price"))["total"]
        or Decimal("0.00")
    )

    # =========================
    # DAILY CHART DATA
    # =========================
    daily = (
        completed_orders
        .annotate(day=TruncDate("created_at"))
        .values("day")
        .annotate(total=Sum("total_price"))
        .order_by("day")
    )

    return Response({
        "total": float(total),
        "weekly": float(weekly),
        "monthly": float(monthly),
        "daily": list(daily),
    })
