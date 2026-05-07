from django.urls import path
from .views import ToggleUserView

from .views import (
    RegisterUserAPIView,
    LoginAPIView,
    LogoutAPIView,
    UserDetailAPIView,
    PasswordResetRequestAPIView,
    PasswordResetConfirmAPIView,
)

from .admin_views import (
    AdminDashboardAPIView,
    AdminUsersAPIView,
)

urlpatterns = [
    # ======================
    # AUTH
    # ======================
    path("register/", RegisterUserAPIView.as_view()),
    path("login/", LoginAPIView.as_view()),
    path("logout/", LogoutAPIView.as_view()),

    # current user
    path("me/", UserDetailAPIView.as_view()),

    # ======================
    # PASSWORD RESET
    # ======================
    path("password-reset/", PasswordResetRequestAPIView.as_view()),
    path(
        "password-reset-confirm/<uid>/<token>/",
        PasswordResetConfirmAPIView.as_view(),
    ),

    # ======================
    # ADMIN
    # ======================
    path("admin/dashboard/", AdminDashboardAPIView.as_view()),
    path("admin/users/<int:user_id>/toggle/", ToggleUserView.as_view()),

    # user management
    path("admin/users/", AdminUsersAPIView.as_view()),
]
