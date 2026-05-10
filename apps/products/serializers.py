from rest_framework import serializers

from .models import Product, MedicineBatch
from apps.pharmacies.models import Pharmacy


# =========================
# MEDICINE BATCH SERIALIZER
# =========================
class MedicineBatchSerializer(serializers.ModelSerializer):
    pharmacy_name = serializers.CharField(
        source="pharmacy.name",
        read_only=True,
    )

    class Meta:
        model = MedicineBatch
        fields = [
            "id",
            "batch_number",
            "price",
            "quantity",
            "pharmacy",
            "pharmacy_name",
            "created_at",
        ]

        extra_kwargs = {
            "pharmacy": {"read_only": True}
        }


# =========================
# PRODUCT SERIALIZER
# =========================
class ProductSerializer(serializers.ModelSerializer):
    batches = MedicineBatchSerializer(many=True, required=False)
    total_stock = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "total_stock",
            "batches",
        ]

    # =========================
    # STOCK PER PHARMACY
    # =========================
    def get_total_stock(self, obj):
        request = self.context.get("request")

        if request and request.user.is_authenticated:
            pharmacy = Pharmacy.objects.filter(owner=request.user).first()
            if pharmacy:
                return obj.total_stock(pharmacy)

        return obj.total_stock()

    # =========================
    # CREATE PRODUCT + BATCHES
    # =========================
    def create(self, validated_data):
        request = self.context.get("request")
        user = request.user

        if not user or not user.is_authenticated:
            raise serializers.ValidationError("Authentication required")

        pharmacy = Pharmacy.objects.filter(owner=user).first()

        if not pharmacy:
            raise serializers.ValidationError("No pharmacy assigned to user")

        batches_data = validated_data.pop("batches", [])

        product = Product.objects.create(**validated_data)

        for batch in batches_data:
            MedicineBatch.objects.create(
                product=product,
                pharmacy=pharmacy,
                batch_number=batch.get("batch_number"),
                quantity=batch.get("quantity", 0),
                price=batch.get("price", 0),
            )

        return product
