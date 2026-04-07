from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import PharmacyViewSet, recommend_products_view, update_location

router = DefaultRouter()
router.register("", PharmacyViewSet)

urlpatterns = [
    path("recommendations/", recommend_products_view, name="recommend_products"),
    path("", include(router.urls)),  # include all router URLs
    path("riders/location/", update_location, name="update_location"),
]
