from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets
from django.shortcuts import get_object_or_404

from .serializers import ProductSerializer
from .models import Product, MedicineBatch


# =========================
# SEARCH MEDICINES
# =========================
@api_view(["GET"])
@permission_classes([AllowAny])
def medicine_search(request):
    query = request.GET.get("q", "")
    pharmacy_id = request.GET.get("pharmacy_id")

    products = Product.objects.filter(name__icontains=query)

    if pharmacy_id:
        products = products.filter(batches__pharmacy_id=pharmacy_id)

    products = products.distinct()

    results = []

    for product in products:
        for batch in product.batches.select_related("pharmacy").all():
            results.append({
                "product_id": product.id,
                "batch_id": batch.id,
                "name": product.name,
                "description": product.description,
                "pharmacy": batch.pharmacy.name if batch.pharmacy else "",
                "pharmacy_id": batch.pharmacy.id if batch.pharmacy else None,
                "price": str(batch.price),
                "stock": batch.quantity,
                "batch_number": batch.batch_number,
            })

    return Response(results)


# =========================
# VIEWSET
# =========================
class MedicineViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()


# =========================
# ADD STOCK
# =========================
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_stock(request):
    batch_id = request.data.get("batch_id")
    quantity = request.data.get("quantity")

    batch = get_object_or_404(MedicineBatch, id=batch_id)

    batch.quantity += int(quantity)
    batch.save()

    return Response({
        "message": "Stock added",
        "new_stock": batch.quantity
    })


# =========================
# REDUCE STOCK
# =========================
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def reduce_stock(request):
    batch_id = request.data.get("batch_id")
    quantity = request.data.get("quantity")

    batch = get_object_or_404(MedicineBatch, id=batch_id)

    qty = int(quantity)

    if qty > batch.quantity:
        return Response({"error": "Not enough stock"}, status=400)

    batch.quantity -= qty
    batch.save()

    return Response({
        "message": "Stock reduced",
        "new_stock": batch.quantity
    })


# =========================
# UPDATE PRICE
# =========================
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def update_price(request):
    batch_id = request.data.get("batch_id")
    price = request.data.get("price")

    batch = get_object_or_404(MedicineBatch, id=batch_id)

    batch.price = price
    batch.save()

    return Response({
        "message": "Price updated",
        "new_price": str(batch.price)
    })


# =========================
# DELETE BATCH (IMPORTANT FIX)
# =========================
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_batch(request):
    batch_id = request.query_params.get("batch_id")

    batch = get_object_or_404(MedicineBatch, id=batch_id)
    batch.delete()

    return Response({
        "message": "Batch deleted"
    })
