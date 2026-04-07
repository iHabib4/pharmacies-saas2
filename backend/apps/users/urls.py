from django.urls import path

from .views import (LogoutAPIView, PasswordResetConfirmAPIView,
                    PasswordResetRequestAPIView, RegisterUserAPIView,
                    UserDetailAPIView)

urlpatterns = [
    # Registration
    path("register/", RegisterUserAPIView.as_view(), name="register"),
    # Logout (token blacklist)
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    # Password reset
    path(
        "password-reset/",
        PasswordResetRequestAPIView.as_view(),
        name="password_reset_request",
    ),
    path(
        "password-reset-confirm/<uid>/<token>/",
        PasswordResetConfirmAPIView.as_view(),
        name="password_reset_confirm",
    ),
    # Current user info
    path("me/", UserDetailAPIView.as_view(), name="user_detail"),
]
