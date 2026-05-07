from rest_framework import serializers
from .models import MedicineBatch, Pharmacy, Product


# =========================
# PHARMACY
# =========================
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


# =========================
# MEDICINE BATCH
# =========================
class MedicineBatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineBatch
        fields = [
            "id",
            "batch_number",
            "price",
            "quantity",
            "pharmacy",
        ]


# =========================
# PRODUCT
# =========================
class ProductSerializer(serializers.ModelSerializer):
    batches = MedicineBatchSerializer(many=True, required=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "batches",
        ]

    def create(self, validated_data):
        batches_data = validated_data.pop("batches", [])

        product = Product.objects.create(**validated_data)

        try:
            for batch in batches_data:
                pharmacy = batch.get("pharmacy")

                if not pharmacy:
                    raise serializers.ValidationError(
                        "Pharmacy is required for each batch"
                    )

                # =========================
                # SAFE PHARMACY HANDLING
                # =========================
                if hasattr(pharmacy, "id"):
                    pharmacy = pharmacy.id

                elif isinstance(pharmacy, dict):
                    pharmacy = pharmacy.get("id")

                elif isinstance(pharmacy, str):
                    pharmacy_obj = Pharmacy.objects.filter(name=pharmacy).first()
                    if not pharmacy_obj:
                        raise serializers.ValidationError(
                            f"Pharmacy '{pharmacy}' not found"
                        )
                    pharmacy = pharmacy_obj.id

                price = batch.get("price")
                quantity = batch.get("quantity")

                if price is None or quantity is None:
                    raise serializers.ValidationError(
                        "price and quantity are required for each batch"
                    )

                MedicineBatch.objects.create(
                    product=product,
                    pharmacy_id=pharmacy,
                    price=price,
                    quantity=quantity,
                    batch_number=batch.get(
                        "batch_number",
                        f"AUTO-{product.id}"
                    )
                )

        except Exception as e:
            # rollback product if anything fails
            product.delete()
            raise serializers.ValidationError(str(e))

        return product
