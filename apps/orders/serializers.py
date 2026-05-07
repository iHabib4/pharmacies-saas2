from rest_framework import serializers
from apps.orders.models import Order, OrderItem


# -------------------------
# ORDER ITEM SERIALIZER
# -------------------------
class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)

    class Meta:
        model = OrderItem
        fields = (
            "id",
            "product_name",
            "quantity",
            "price",
        )


# -------------------------
# ORDER SERIALIZER
# -------------------------
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    pharmacy_name = serializers.CharField(
        source="pharmacy.name",
        read_only=True,
    )

    customer_name = serializers.CharField(
        source="consumer.first_name",
        read_only=True,
    )

    class Meta:
        model = Order
        fields = (
            "id",
            "customer_name",
            "pharmacy_name",
            "total_price",
            "status",
            "created_at",
            "items",
        )
