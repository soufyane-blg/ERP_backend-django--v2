# serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterSerializer(serializers.Serializer):

    email = serializers.EmailField()

    password = serializers.CharField(
        write_only=True,
        min_length=6,
        trim_whitespace=False
    )

    organization_name = serializers.CharField(
        max_length=100
    )

    role = serializers.ChoiceField(
        choices=["admin", "staff"],
        default="staff"
    )

    def validate_email(self, value):

        value = value.lower()

        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Email already exists"
            )

        return value


class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()

    password = serializers.CharField(
        trim_whitespace=False
    )


class LogoutSerializer(serializers.Serializer):

    refresh = serializers.CharField()