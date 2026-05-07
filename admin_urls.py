from django.urls import path
from .admin_views import (
    AdminDashboardAPIView,
    AdminUsersAPIView,
    AdminUserUpdateAPIView,
)

urlpatterns = [
    path("dashboard/", AdminDashboardAPIView.as_view()),
    path("users/", AdminUsersAPIView.as_view()),
    path("users/<int:pk>/", AdminUserUpdateAPIView.as_view()),
]
