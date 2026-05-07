from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import RiderViewSet, register_rider, update_location

router = DefaultRouter()
router.register("", RiderViewSet, basename="riders")

urlpatterns = [
    # 🔓 Public
    path("register/", register_rider, name="register_rider"),
    # 🔐 Protected
    path("location/", update_location, name="update_location"),
    # 📦 ViewSet
    path("", include(router.urls)),
]
