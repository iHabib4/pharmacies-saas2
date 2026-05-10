from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    MedicineViewSet,
    medicine_search,
    customer_medicine_feed,
    add_stock,
    reduce_stock,
    update_price,
    delete_batch,
)

router = DefaultRouter()
router.register(r"medicines", MedicineViewSet, basename="medicines")

urlpatterns = [
    # PUBLIC MARKETPLACE
    path("marketplace/medicines/", customer_medicine_feed),

    # SEARCH
    path("medicines/search/", medicine_search),

    # STOCK MANAGEMENT
    path("batch/add-stock/", add_stock),
    path("batch/reduce-stock/", reduce_stock),
    path("batch/update-price/", update_price),
    path("batch/delete/", delete_batch),

    # CRUD ROUTER
    path("", include(router.urls)),
]
