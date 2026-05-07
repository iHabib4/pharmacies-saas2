# apps/deliveries/urls.py

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (DeliveryTrackingViewSet, OrderViewSet, accept_delivery,
                    available_deliveries, confirm_delivery,
                    update_delivery_status)

# ===============================
# DRF routers
# ===============================
router = DefaultRouter()
router.register(r"orders", OrderViewSet, basename="orders")
router.register(r"tracking", DeliveryTrackingViewSet, basename="tracking")

# ===============================
# API endpoints
# ===============================
urlpatterns = [
    # Rider actions
    path("available/", available_deliveries, name="available_deliveries"),
    path("accept/<int:delivery_id>/", accept_delivery, name="accept_delivery"),
    path(
        "update-status/<int:delivery_id>/",
        update_delivery_status,
        name="update_delivery_status",
    ),
    # Confirm delivery
    path("confirm/<int:delivery_id>/", confirm_delivery, name="confirm_delivery"),
]

# ===============================
# Include router URLs
# ===============================
urlpatterns += router.urls
