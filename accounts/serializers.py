from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=6, trim_whitespace=False)
    organization_name = serializers.CharField(max_length=100)

    role = serializers.ChoiceField(
        choices=["admin", "staff"],
        default="staff"
    )

    def validate_username(self, value):
        if " " in value:
            raise serializers.ValidationError("Username cannot contain spaces")

        return value

    def validate_email(self, value):
        value = value.lower()

        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")

        return value
    
    def validate(self, data):
        if data.get("password") == data.get("username"):
            raise serializers.ValidationError("Password cannot be same as username")
        return data

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)



class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    
