import requests
from django.conf import settings


def calculate_fastest_route(pharmacy_location, customer_location):
    url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": f"{pharmacy_location[0]},{pharmacy_location[1]}",
        "destination": f"{customer_location[0]},{customer_location[1]}",
        "key": settings.GOOGLE_MAPS_API_KEY,
        "mode": "driving",
        "departure_time": "now",
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data["status"] != "OK":
        raise Exception(f"Route API error: {data['status']}")

    route = data["routes"][0]["legs"][0]

    return {
        "distance_km": route["distance"]["value"] / 1000,
        "duration_min": route["duration"]["value"] / 60,
        "traffic_duration_min": route.get("duration_in_traffic", {}).get(
            "value", route["duration"]["value"]
        )
        / 60,
    }
