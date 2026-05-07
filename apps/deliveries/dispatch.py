from apps.riders.models import Rider
from core.utils import calculate_distance


def find_best_rider(lat, lon):

    riders = Rider.objects.filter(is_available=True)

    best_rider = None
    best_score = 0

    for rider in riders:

        distance = calculate_distance(lat, lon, rider.latitude, rider.longitude)

        distance_score = max(0, 10 - distance)

        rating_score = rider.rating

        workload_score = max(0, 10 - rider.total_deliveries)

        score = distance_score * 0.4 + rating_score * 0.3 + workload_score * 0.3

        if score > best_score:
            best_score = score
            best_rider = rider

    return best_rider
