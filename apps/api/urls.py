from django.urls import include, path

urlpatterns = [
    path("deliveries/", include("apps.deliveries.urls")),
]
