from core.utils import calculate_distance

from .models import Product


def search_medicines(query, user_lat, user_lon):

    products = Product.objects.filter(
        name__icontains=query, is_available=True, stock__gt=0
    )

    results = []

    for product in products:

        pharmacy = product.pharmacy

        distance = calculate_distance(
            user_lat, user_lon, pharmacy.latitude, pharmacy.longitude
        )

        results.append({"product": product, "distance": distance})

    results.sort(key=lambda x: (x["distance"], x["product"].price))

    return results


from datetime import date


def get_valid_batches(product):

    batches = product.batches.filter(expiry_date__gt=date.today(), quantity__gt=0)

    return batches


def get_next_batch(product):
    """
    Return the batch with the earliest expiry date that has stock.
    """
    return (
        product.batches.filter(expiry_date__gt=date.today(), quantity__gt=0)
        .order_by("expiry_date")
        .first()
    )


def check_low_stock(product):
    """
    Returns True if total stock of a product is below its low_stock_threshold.
    """
    total_stock = sum(batch.quantity for batch in product.batches.all())
    return total_stock < product.low_stock_threshold
