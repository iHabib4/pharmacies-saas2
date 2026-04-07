from django.urls import include, path

from .views import register

urlpatterns = [
    path("deliveries/", include("apps.deliveries.urls")),
    path("register/", register, name="register"),
]
