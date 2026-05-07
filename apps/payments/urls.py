# apps/payments/urls.py

from django.urls import path

from .views import mobile_money_payment, mobile_money_callback

app_name = "payments"

urlpatterns = [
    path("mobile-money/initiate/", mobile_money_payment, name="mobile-money-initiate"),
    path("mobile-money/callback/", mobile_money_callback, name="mobile-money-callback"),
]
