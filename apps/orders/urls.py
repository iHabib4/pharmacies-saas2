from django.urls import path

from .views import (
    create_order_view,
    get_order_eta,
    confirm_delivery,
    pharmacy_revenue_view,
    rider_performance,
    list_orders,
)

app_name = "orders"

urlpatterns = [
    path("", list_orders, name="list_orders"),
    path("create/", create_order_view, name="create_order"),
    path("<int:order_id>/eta/", get_order_eta, name="get_order_eta"),
    path("<int:order_id>/confirm/", confirm_delivery, name="confirm_delivery"),
    path("analytics/pharmacy-revenue/", pharmacy_revenue_view),
    path("analytics/riders/", rider_performance),
]
