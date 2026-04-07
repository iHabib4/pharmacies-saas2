# core/utils.py

import math
from typing import Dict, List, Optional

from apps.deliveries.models import Delivery  # assuming Delivery model exists
from apps.orders.models import Order  # assuming Order model exists
from apps.riders.models import Rider
from apps.tracking.models import RiderLocation


def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate distance between two lat/lng points in kilometers.
    """
    R = 6371  # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def find_nearby_riders(lat: float, lon: float, radius: float = 5) -> List[Rider]:
    """
    Return a list of Rider objects that are available and within `radius` km.
    Uses RiderLocation for real-time positions.
    """
    riders_locations = RiderLocation.objects.select_related("rider")
    nearby_riders = []

    for location in riders_locations:
        if location.latitude is not None and location.longitude is not None:
            distance = calculate_distance(
                lat, lon, location.latitude, location.longitude
            )
            if distance <= radius and location.rider.is_available:
                nearby_riders.append((location.rider, distance))

    # Sort by distance
    nearby_riders.sort(key=lambda x: x[1])
    return [rider for rider, _ in nearby_riders]


def assign_rider(order: Order, radius: float = 5) -> Optional[Delivery]:
    """
    Assigns the nearest available rider to the order within the given radius.
    Returns the created Delivery object or None if no rider is available.
    """
    pharmacy = order.pharmacy
    nearby_riders = find_nearby_riders(pharmacy.latitude, pharmacy.longitude, radius)

    if not nearby_riders:
        return None  # No available rider nearby

    # Pick the closest rider
    rider = nearby_riders[0]

    # Create the Delivery object
    delivery = Delivery.objects.create(order=order, rider=rider, status="assigned")

    # Mark rider as unavailable
    rider.is_available = False
    rider.save(update_fields=["is_available"])

    return delivery


def calculate_commission(order: Order) -> Dict[str, float]:
    """
    Returns the admin and pharmacy share for an order.
    """
    admin_percent = 0.1  # 10% commission
    admin_share = order.total_price * admin_percent
    pharmacy_share = order.total_price - admin_share

    return {"admin_share": admin_share, "pharmacy_share": pharmacy_share}


def find_nearest_riders(
    lat: float, lon: float, radius: float = 5, limit: int = 5
) -> List[Dict]:
    """
    Returns a list of dictionaries with nearest available riders and their distance.
    Uses the Rider model's latitude and longitude fields directly.
    """
    riders = Rider.objects.filter(is_available=True)
    nearby = []

    for rider in riders:
        if rider.latitude is not None and rider.longitude is not None:
            distance = calculate_distance(lat, lon, rider.latitude, rider.longitude)
            if distance <= radius:
                nearby.append({"rider": rider, "distance": distance})

    # Sort by distance
    nearby.sort(key=lambda x: x["distance"])
    return nearby[:limit]
