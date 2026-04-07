# apps/products/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from core.utils import calculate_distance

from .models import MedicineBatch, Product
from .serializers import ProductSerializer


@api_view(["GET"])
@permission_classes([AllowAny])
def medicine_search(request):
    """
    Search products with optional filters:
    - q: product name
    - price_min / price_max
    - max_distance (km)
    - lat / lon
    - open_pharmacies=true
    - delivery_time (minutes)
    """
    query = request.GET.get("q", "")
    lat = request.GET.get("lat")
    lon = request.GET.get("lon")
    price_min = request.GET.get("price_min")
    price_max = request.GET.get("price_max")
    max_distance = request.GET.get("max_distance")
    open_pharmacies = request.GET.get("open_pharmacies")
    delivery_time = request.GET.get("delivery_time")

    products = Product.objects.filter(name__icontains=query)
    results = []

    for product in products:
        for batch in product.batches.all():
            pharmacy = batch.pharmacy

            # Open pharmacy filter
            if open_pharmacies == "true" and not pharmacy.is_open:
                continue

            # Delivery time filter
            if delivery_time and pharmacy.estimated_delivery_time > int(delivery_time):
                continue

            # Distance filter
            if lat and lon and max_distance:
                if pharmacy.latitude and pharmacy.longitude:
                    distance = calculate_distance(
                        float(lat), float(lon), pharmacy.latitude, pharmacy.longitude
                    )
                    if distance > float(max_distance):
                        continue

            # Price filter
            if price_min and batch.price < float(price_min):
                continue
            if price_max and batch.price > float(price_max):
                continue

            results.append(
                {
                    "product_id": product.id,
                    "name": product.name,
                    "description": product.description,
                    "pharmacy": pharmacy.name,
                    "pharmacy_id": pharmacy.id,
                    "price": batch.price,
                    "stock": batch.quantity,
                    "batch_number": batch.batch_number,
                }
            )

    return Response(results)
