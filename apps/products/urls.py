from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    MedicineViewSet,
    medicine_search,
    add_stock,
    reduce_stock,
    update_price,
    delete_batch,
)

router = DefaultRouter()
router.register(r"medicines", MedicineViewSet, basename="medicines")

urlpatterns = [
    path("medicines/search/", medicine_search),

    # STOCK ACTIONS
    path("batch/add-stock/", add_stock),
    path("batch/reduce-stock/", reduce_stock),
    path("batch/update-price/", update_price),
    path("batch/delete/", delete_batch),

    path("", include(router.urls)),
]
