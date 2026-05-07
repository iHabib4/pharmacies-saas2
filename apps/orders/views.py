from decimal import Decimal

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import OrderSerializer
from apps.deliveries.models import Delivery
from apps.pharmacies.models import Pharmacy
from apps.products.models import MedicineBatch, Product
from apps.orders.models import Order, OrderItem


# ------------------------------
# 1️⃣ CREATE ORDER
# ------------------------------
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_order_view(request):
    data = request.data
    items = data.get("items")
    delivery_address = data.get("delivery_address")
    pharmacy_id = data.get("pharmacy_id")

    if not items or not delivery_address or not pharmacy_id:
        return Response(
            {"error": "items, delivery_address, and pharmacy_id are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        pharmacy = Pharmacy.objects.get(id=pharmacy_id)
    except Pharmacy.DoesNotExist:
        return Response(
            {"error": "Pharmacy not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    order = Order.objects.create(
        consumer=request.user,
        pharmacy=pharmacy,
        delivery_address=delivery_address,
        total_price=Decimal("0.00"),
        status="pending",
    )

    total_price = Decimal("0.00")

    for item in items:
        product_id = item.get("product_id")
        quantity = int(item.get("quantity", 1))

        if not product_id or quantity <= 0:
            return Response(
                {"error": "Invalid product_id or quantity"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(
                {"error": f"Product {product_id} not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        batch = (
            MedicineBatch.objects.filter(
                product=product,
                pharmacy_id=pharmacy.id,
                quantity__gt=0,
            )
            .order_by("id")
            .first()
        )

        if not batch:
            return Response(
                {"error": f"{product.name} is out of stock"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if batch.quantity < quantity:
            return Response(
                {
                    "error": f"Only {batch.quantity} units available for {product.name}"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        price = batch.price * quantity
        total_price += price

        # reduce stock
        batch.quantity -= quantity
        batch.save()

        OrderItem.objects.create(
            order=order,
            product=product,
            batch=batch,
            quantity=quantity,
            price=price,
        )

    order.total_price = total_price
    order.save()

    # create delivery record
    Delivery.objects.create(order=order, pharmacy=pharmacy, status="pending")

    return Response(
        {
            "message": "Order created successfully",
            "order_id": order.id,
            "total_price": float(total_price),
        },
        status=status.HTTP_201_CREATED,
    )


# ------------------------------
# 2️⃣ GET ORDER ETA
# ------------------------------
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_order_eta(request, order_id: int):
    try:
        order = Order.objects.get(id=order_id, consumer=request.user)

        return Response(
            {
                "order_id": order.id,
                "eta_minutes": 30,
            }
        )

    except Order.DoesNotExist:
        return Response(
            {"error": "Order not found"},
            status=status.HTTP_404_NOT_FOUND,
        )
# ------------------------------
# 3️⃣ RIDER PERFORMANCE
# ------------------------------
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def rider_performance(request, rider_id: int):
    return Response(
        {
            "rider_id": rider_id,
            "completed_orders": 50,
            "average_delivery_time": 28,
        }
    )


# ------------------------------
# 4️⃣ CONFIRM DELIVERY
# ------------------------------
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def confirm_delivery(request, order_id: int):
    try:
        order = Order.objects.get(id=order_id, consumer=request.user)

        if order.status == "completed":
            return Response({"message": "Order already delivered"})

        order.status = "completed"
        order.save()

        return Response(
            {"message": f"Order {order_id} marked as delivered"}
        )

    except Order.DoesNotExist:
        return Response(
            {"error": "Order not found"},
            status=status.HTTP_404_NOT_FOUND,
        )


# ------------------------------
# 5️⃣ PHARMACY REVENUE
# ------------------------------
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def pharmacy_revenue_view(request):
    user = request.user

    try:
        pharmacy = Pharmacy.objects.get(owner=user)
    except Pharmacy.DoesNotExist:
        return Response(
            {"error": "You do not own a pharmacy"},
            status=status.HTTP_403_FORBIDDEN,
        )

    orders = Order.objects.filter(
        pharmacy=pharmacy,
        status="completed",
    )

    total_sales = sum(order.total_price for order in orders)

    commission_rate = Decimal("0.10")
    commission = total_sales * commission_rate

    return Response(
        {
            "pharmacy_id": pharmacy.id,
            "pharmacy_name": pharmacy.name,
            "total_sales": float(total_sales),
            "commission_deducted": float(commission),
        }
    )

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_orders(request):
    orders = Order.objects.filter(consumer=request.user).order_by("-created_at")
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_orders(request):
    user = request.user

    # pharmacy owner sees pharmacy orders
    if hasattr(user, "pharmacy"):
        orders = Order.objects.filter(pharmacy=user.pharmacy)
    else:
        orders = Order.objects.filter(consumer=user)

    serializer = OrderSerializer(
        orders.order_by("-created_at"),
        many=True
    )

    return Response(serializer.data)

