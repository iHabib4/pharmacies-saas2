from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "mobile_number",
            "role",
            "is_superuser",
            "is_staff",
        ]


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["mobile_number", "password", "role"]

    def create(self, validated_data):
        user = User.objects.create_user(
            mobile_number=validated_data["mobile_number"],
            password=validated_data["password"],
            role=validated_data.get("role", "customer"),
        )
        return user
