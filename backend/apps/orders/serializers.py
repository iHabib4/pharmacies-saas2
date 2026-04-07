from rest_framework import serializers

from apps.orders.models import Order, OrderItem
from apps.products.models import MedicineBatch, Product


# Product + Batch Serializer
class MedicineBatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineBatch
        fields = ("id", "batch_number", "expiry_date", "quantity", "price")


class ProductSerializer(serializers.ModelSerializer):
    batches = MedicineBatchSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "description",
            "is_available",
            "low_stock_threshold",
            "is_otc",
            "pharmacy",
            "batches",
        )


# OrderItem Serializer
class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    batch = MedicineBatchSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ("id", "product", "batch", "quantity", "price")


# Order Serializer
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    consumer_name = serializers.CharField(source="consumer.first_name", read_only=True)
    pharmacy_name = serializers.CharField(source="pharmacy.name", read_only=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "consumer",
            "consumer_name",
            "pharmacy",
            "pharmacy_name",
            "total_price",
            "status",
            "created_at",
            "completed_at",
            "items",
        )
