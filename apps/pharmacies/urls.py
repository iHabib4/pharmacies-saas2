from django.urls import include, path
from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import pharmacy_stats

urlpatterns = [
    path("stats/", pharmacy_stats),
]

from .views import (
    PharmacyViewSet,
    recommend_products_view,
    update_location
)

router = DefaultRouter()
router.register("", PharmacyViewSet)

urlpatterns = [
    path(
        "recommendations/",
        recommend_products_view,
        name="recommend_products"
    ),

    path(
        "riders/location/",
        update_location,
        name="update_location"
    ),

    # include all router URLs (CRUD for PharmacyViewSet)
    path("", include(router.urls)),
]
