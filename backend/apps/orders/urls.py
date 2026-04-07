# apps/orders/urls.py

from django.urls import path

from .views import (confirm_delivery, create_order_view, get_order_eta,
                    pharmacy_revenue_view, rider_performance)

app_name = "orders"

urlpatterns = [
    path("orders/<int:order_id>/eta/", get_order_eta, name="get_order_eta"),
    path("analytics/riders/", rider_performance, name="rider_performance"),
    path("create-order/", create_order_view, name="create_order"),
    path("orders/<int:order_id>/confirm/", confirm_delivery, name="confirm_delivery"),
    path("analytics/pharmacy-revenue/", pharmacy_revenue_view, name="pharmacy_revenue"),
]
