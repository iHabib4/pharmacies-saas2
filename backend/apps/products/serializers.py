# apps/products/serializers.py

from rest_framework import serializers

from .models import MedicineBatch, Pharmacy, Product


class PharmacySerializer(serializers.ModelSerializer):
    class Meta:
        model = Pharmacy
        fields = [
            "id",
            "name",
            "latitude",
            "longitude",
            "is_open",
            "estimated_delivery_time",
        ]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "description"]


class MedicineBatchSerializer(serializers.ModelSerializer):
    # Use product and pharmacy names directly
    product_name = serializers.CharField(source="product.name", read_only=True)
    pharmacy_name = serializers.CharField(source="pharmacy.name", read_only=True)

    class Meta:
        model = MedicineBatch
        fields = [
            "id",
            "batch_number",
            "price",
            "quantity",
            "product_name",
            "pharmacy_name",
        ]
