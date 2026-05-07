from geopy.distance import geodesic


def distance_km(coord1, coord2):
    """
    coord1 and coord2 are tuples: (latitude, longitude)
    Returns distance in kilometers.
    """
    return geodesic(coord1, coord2).km


def calculate_eta(distance_km, traffic_level="medium"):
    """
    Estimate time in minutes.
    traffic_level: "low", "medium", "high"
    """
    # Average speeds in km/h
    traffic_speeds = {"low": 40, "medium": 25, "high": 15}
    speed = traffic_speeds.get(traffic_level, 25)  # default to medium
    eta_minutes = (distance_km / speed) * 60
    return round(eta_minutes)
