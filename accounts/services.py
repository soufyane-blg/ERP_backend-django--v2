from django.contrib.auth import get_user_model, authenticate
from django.db import transaction

from rest_framework.exceptions import ValidationError

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from .models import Organization

User = get_user_model()


@transaction.atomic
def register_user(
    username: str,
    email: str,
    password: str,
    organization_name: str,
    role: str
):

    if User.objects.filter(username=username).exists():
        raise ValidationError("Username already exists")

    if User.objects.filter(email=email).exists():
        raise ValidationError("Email already exists")

    organization, _ = Organization.objects.get_or_create(
        name=organization_name,
        defaults={
            "email": email,
            "address": ""
        }
    )

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        organization=organization
    )

    user.role = role
    user.save(update_fields=["role"])

    return {
        "id": user.id,
        "username": user.username,
        "organization": organization.name,
    }


def login_user(username: str, password: str):

    user = authenticate(
        username=username,
        password=password
    )

    if not user:
        raise ValidationError("Invalid username or password")

    if not user.is_active:
        raise ValidationError("User is inactive")

    return user


def generate_tokens(user):

    refresh = RefreshToken.for_user(user)

    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }


def login_service(username: str, password: str):

    user = login_user(username, password)

    tokens = generate_tokens(user)

    return {
        "user_id": user.id,
        "username": user.username,
        "access": tokens["access"],
        "refresh": tokens["refresh"],
    }


def refresh_tokens_service(refresh_token: str):

    try:
        token = RefreshToken(refresh_token)

        return {
            "access": str(token.access_token),
            "refresh": str(token),
        }

    except TokenError:
        raise ValidationError("Invalid or expired refresh token")


def get_current_user(user):

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "organization": user.organization.name,
    }


def logout_service(refresh_token: str):

    try:
        token = RefreshToken(refresh_token)

        token.blacklist()

    except TokenError:
        raise ValidationError("Invalid or expired token")