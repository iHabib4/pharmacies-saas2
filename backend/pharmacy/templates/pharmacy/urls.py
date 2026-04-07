from django.urls import path

from . import views

urlpatterns = [
    path("dashboard/", views.pharmacy_dashboard, name="pharmacy-dashboard"),
]
