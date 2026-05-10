# apps/orders/urls.py

from django.urls import path

from .views import (
    create_order_view,
    get_order_eta,
    confirm_delivery,
    pharmacy_revenue_view,
    rider_performance,
    list_orders,
    get_orders,
    earnings_analytics,
)

app_name = "orders"

urlpatterns = [

    # =========================
    # ORDERS
    # =========================
    path(
        "",
        list_orders,
        name="list_orders",
    ),

    path(
        "my-orders/",
        get_orders,
        name="my_orders",
    ),

    path(
        "create/",
        create_order_view,
        name="create_order",
    ),

    # =========================
    # DELIVERY
    # =========================
    path(
        "<int:order_id>/eta/",
        get_order_eta,
        name="get_order_eta",
    ),

    path(
        "<int:order_id>/confirm/",
        confirm_delivery,
        name="confirm_delivery",
    ),

    # =========================
    # ANALYTICS
    # =========================
    path(
        "analytics/pharmacy-revenue/",
        pharmacy_revenue_view,
        name="pharmacy_revenue",
    ),

    path(
        "analytics/earnings/",
        earnings_analytics,
        name="earnings_analytics",
    ),

    path(
        "analytics/riders/",
        rider_performance,
        name="rider_performance",
    ),
]
