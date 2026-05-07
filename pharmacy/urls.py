# pharmacy/urls.py
from django.urls import path

from .views import admin_dashboard, marketplace, search_medicine

urlpatterns = [
    path("admin-dashboard/", admin_dashboard, name="admin-dashboard"),
    path("admin-dashboard-page/", admin_dashboard_page, name="admin-dashboard-page"),
    path("marketplace/", marketplace, name="marketplace"),
    path("search/", search_medicine, name="search-medicine"),
]
