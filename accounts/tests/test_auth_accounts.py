import pytest
from rest_framework import status


@pytest.mark.django_db
def test_login_success(user, api_client):

    
    data = {
        "email": user.email,
        "password": "StrongPass123"
    }

    response = api_client.post("/api/auth/login/", data)

    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data
    assert "refresh_token" in response.cookies

@pytest.mark.django_db
def test_login_with_wrong_password(user, api_client):

    

    data = {
        "email": user.email,
        "password": "WrongPassword"
    }

    response = api_client.post("/api/auth/login/", data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_login_missing_password(user, api_client):

    

    data = {
        "email": user.email
    }

    response = api_client.post("/api/auth/login/", data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_login_missing_email(user, api_client):

    

    data = {
        "password": "StrongPass123"
    }

    response = api_client.post("/api/auth/login/", data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST

@pytest.mark.django_db
def test_user_does_not_exist(api_client):

    

    data = {
        "email": "nonexistent@example.com",
        "password": "StrongPass123"
    }

    response = api_client.post("/api/auth/login/", data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED