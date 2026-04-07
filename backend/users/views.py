# users/views.py

from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import UserRegistrationSerializer


class RegisterUserView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "message": "User registered successfully",
                "user_id": user.id,
                "mobile_number": user.mobile_number,
            },
            status=status.HTTP_201_CREATED,
        )
