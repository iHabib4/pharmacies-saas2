# apps/pharmacies/dispatch.py

from math import atan2, cos, radians, sin, sqrt

from apps.riders.models import Rider


def find_best_rider(lat, lon):
    """
    Simple example: finds the closest available rider to the given coordinates.
    Returns a Rider object or None.
    """

    def distance(lat1, lon1, lat2, lon2):
        # Haversine formula
        R = 6371  # Earth radius in km
        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)
        a = (
            sin(dlat / 2) ** 2
            + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
        )
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return R * c

    riders = Rider.objects.filter(is_available=True)
    if not riders.exists():
        return None

    # find nearest rider
    best_rider = min(
        riders, key=lambda r: distance(lat, lon, r.latitude or 0, r.longitude or 0)
    )
    return best_rider
