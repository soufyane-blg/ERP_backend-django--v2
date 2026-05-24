import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

User = get_user_model()


@pytest.mark.django_db
def test_registration_success(api_client):

    url = reverse("registration-view")

    data = {
    "email": "test@example.com",
    "password": "StrongPass123",
    "organization_name": "Test Org",
    "role": "admin",
}

    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_201_CREATED

    assert User.objects.filter(email=data["email"]).exists()
    assert User.objects.count() == 1

    created_user = User.objects.get(email=data["email"])

    assert created_user.check_password(data["password"])


@pytest.mark.django_db
def test_registration_returns_400_for_existing_email(api_client, user):

    url = reverse("registration-view")

    data = {
        "email": user.email,
        "password": "AnotherPass123",
        "organization_name" : "Test Org",
        "role": "admin",
    }

    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # only fixture user should exist
    assert User.objects.count() == 1

    assert "email" in response.data


@pytest.mark.django_db
def test_registration_returns_400_when_email_missing(api_client):

    url = reverse("registration-view")

    data = {
        "password": "StrongPass123",
        "organization_name": "Test Org",
        "role": "admin",
    }

    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    assert User.objects.count() == 0
    assert "email" in response.data


@pytest.mark.django_db
def test_registration_returns_400_when_password_missing(api_client):

    url = reverse("registration-view")

    data = {
        "email": "newuser@example.com",
        "organization_name": "Test Org",
        "role": "admin",
    }

    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    assert User.objects.count() == 0
    assert "password" in response.data


@pytest.mark.django_db
def test_registration_returns_400_for_invalid_email(api_client):

    url = reverse("registration-view")

    data = {
        "email": "not_valid_email",
        "password": "StrongPass123",
        "organization_name": "Test Org",
        "role": "admin",
    }

    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    assert User.objects.count() == 0
    assert "email" in response.data


@pytest.mark.django_db
def test_registration_returns_400_for_empty_fields(api_client):

    url = reverse("registration-view")

    data = {
        "email": "",
        "password": "",
        "organization_name": "",
        "role": ""
    }

    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    assert User.objects.count() == 0

    assert "email" in response.data
    assert "password" in response.data