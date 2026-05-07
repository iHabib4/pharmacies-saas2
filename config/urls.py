from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path


def home(request):
    return JsonResponse({
        "message": "Django is running 🚀"
    })


urlpatterns = [
    path("", home),
    path("admin/", admin.site.urls),

    # USERS API
    path("api/users/", include("apps.users.urls")),

    # PRODUCTS / MEDICINES API
    path("api/products/", include("apps.products.urls")),

    # CORE API (optional)
    path("api/", include("api.urls")),

    path("api/pharmacies/", include("apps.pharmacies.urls")),
]
