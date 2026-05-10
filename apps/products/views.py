from django.shortcuts import get_object_or_404
from django.db.models import F

from rest_framework import viewsets, serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from core.permissions import (
    IsAdmin,
    IsPharmacy,
    CanManageProducts
)

from apps.pharmacies.models import Pharmacy
from .models import Product, MedicineBatch
from .serializers import ProductSerializer


# =========================
# CUSTOMER MARKETPLACE FEED (GLOBAL)
# =========================
@api_view(["GET"])
@permission_classes([AllowAny])
def customer_medicine_feed(request):
    query = request.GET.get("q", "")

    batches = MedicineBatch.objects.select_related("product", "pharmacy").all()

    if query:
        batches = batches.filter(product__name__icontains=query)

    results = []

    for batch in batches:
        results.append({
            "product_id": batch.product.id,
            "name": batch.product.name,
            "description": batch.product.description,

            "batch_id": batch.id,
            "batch_number": batch.batch_number,

            "price": float(batch.price),
            "stock": batch.quantity,

            "pharmacy_id": batch.pharmacy.id,
            "pharmacy": batch.pharmacy.name,
        })

    results.sort(key=lambda x: x["price"])

    return Response(results)

# =========================
# GET USER PHARMACY
# =========================
def get_user_pharmacy(user):
    """
    Assumes: Pharmacy.owner = FK to User
    """
    return Pharmacy.objects.filter(owner=user).first()


# =========================
# MEDICINE SEARCH (SCOPED FOR PHARMACY STAFF)
# =========================
@api_view(["GET"])
@permission_classes([AllowAny])
def medicine_search(request):
    query = request.GET.get("q", "")

    if request.user.is_authenticated:
        pharmacy = get_user_pharmacy(request.user)

        if not pharmacy:
            return Response([])

        products = Product.objects.filter(
            name__icontains=query,
            batches__pharmacy=pharmacy
        ).distinct()
    else:
        products = Product.objects.filter(name__icontains=query)

    results = []

    for product in products:
        batches = product.batches.select_related("pharmacy").all()

        for batch in batches:
            results.append({
                "product_id": product.id,
                "batch_id": batch.id,
                "name": product.name,
                "description": product.description,
                "pharmacy": batch.pharmacy.name,
                "pharmacy_id": batch.pharmacy.id,
                "price": str(batch.price),
                "stock": batch.quantity,
                "batch_number": batch.batch_number,
            })

    return Response(results)


# =========================
# MEDICINE VIEWSET (PHARMACY ONLY)
# =========================
class MedicineViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    permission_classes = [CanManageProducts]

    def get_queryset(self):
        pharmacy = get_user_pharmacy(self.request.user)

        if not pharmacy:
            return Product.objects.none()

        return Product.objects.filter(
            batches__pharmacy=pharmacy
        ).distinct()

    def get_serializer_context(self):
        return {"request": self.request}

    def perform_create(self, serializer):
        pharmacy = get_user_pharmacy(self.request.user)

        if not pharmacy:
            raise serializers.ValidationError(
                {"error": "No pharmacy is assigned to this user"}
            )

        serializer.save()


# =========================
# ADD STOCK
# =========================
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_stock(request):
    pharmacy = get_user_pharmacy(request.user)

    if not pharmacy:
        return Response({"error": "Invalid pharmacy"}, status=403)

    batch = get_object_or_404(
        MedicineBatch,
        id=request.data.get("batch_id"),
        pharmacy=pharmacy,
    )

    batch.quantity += int(request.data.get("quantity", 0))
    batch.save()

    return Response({
        "message": "Stock added",
        "new_stock": batch.quantity,
    })


# =========================
# REDUCE STOCK
# =========================
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def reduce_stock(request):
    pharmacy = get_user_pharmacy(request.user)

    if not pharmacy:
        return Response({"error": "Invalid pharmacy"}, status=403)

    batch = get_object_or_404(
        MedicineBatch,
        id=request.data.get("batch_id"),
        pharmacy=pharmacy,
    )

    qty = int(request.data.get("quantity", 0))

    if qty > batch.quantity:
        return Response({"error": "Not enough stock"}, status=400)

    batch.quantity -= qty
    batch.save()

    return Response({
        "message": "Stock reduced",
        "new_stock": batch.quantity,
    })


# =========================
# UPDATE PRICE
# =========================
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def update_price(request):
    pharmacy = get_user_pharmacy(request.user)

    if not pharmacy:
        return Response({"error": "Invalid pharmacy"}, status=403)

    batch = get_object_or_404(
        MedicineBatch,
        id=request.data.get("batch_id"),
        pharmacy=pharmacy,
    )

    batch.price = request.data.get("price")
    batch.save()

    return Response({
        "message": "Price updated",
        "new_price": str(batch.price),
    })


# =========================
# DELETE BATCH
# =========================
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_batch(request):
    pharmacy = get_user_pharmacy(request.user)

    if not pharmacy:
        return Response({"error": "Invalid pharmacy"}, status=403)

    batch = get_object_or_404(
        MedicineBatch,
        id=request.query_params.get("batch_id"),
        pharmacy=pharmacy,
    )

    batch.delete()

    return Response({"message": "Batch deleted"})
