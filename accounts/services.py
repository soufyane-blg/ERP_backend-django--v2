# services.py

from django.contrib.auth import get_user_model, authenticate
from django.db import transaction

from rest_framework.exceptions import AuthenticationFailed, ValidationError

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from .models import Organization

User = get_user_model()


@transaction.atomic
def register_user(
    email: str,
    password: str,
    organization_name: str,
    role: str
):

    if User.objects.filter(email=email).exists():
        raise ValidationError("Email already exists")

    organization, _ = Organization.objects.get_or_create(
        name=organization_name,
        defaults={
            "email": email,
            "address": ""
        }
    )

    # username required because you still use AbstractUser
    user = User.objects.create_user(
        username=email,
        email=email,
        password=password,
        organization=organization
    )

    user.role = role

    if role == "admin":
        user.is_staff = True

    user.save(
        update_fields=[
            "role",
            "is_staff",
        ]
    )

    return {
        "id": user.id,
        "email": user.email,
        "organization": organization.name,
    }


def login_user(email: str, password: str):

    # authenticate uses username internally
    user = authenticate(
        username=email,
        password=password
    )

    if not user:
        raise AuthenticationFailed("Invalid email or password")

    if not user.is_active:
        raise AuthenticationFailed("User is inactive")

    return user


def generate_tokens(user):

    refresh = RefreshToken.for_user(user)

    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }


def login_service(email: str, password: str):

    user = login_user(email, password)

    tokens = generate_tokens(user)

    return {
    "user_id": user.id,
    "username": user.username,
    "email": user.email,
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
        "email": user.email,
        "organization": user.organization.name,
    }


def logout_service(refresh_token: str):

    try:
        token = RefreshToken(refresh_token)
        token.blacklist()

    except TokenError:
        raise ValidationError("Invalid or expired token")