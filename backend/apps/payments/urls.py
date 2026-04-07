# apps/payments/urls.py
from django.urls import path

from .views import mobile_money_callback, mobile_money_payment

urlpatterns = [
    path("mobile-money/", mobile_money_payment, name="mobile-money-payment"),
    path("callback/", mobile_money_callback, name="mobile-money-callback"),
]
