import pytest
from django.urls import reverse
from rest_framework import status  



@pytest.mark.django_db
def test_authenticated_user_can_access_Me_view(api_client, user):

    api_client.force_authenticate(user=user)

    url = reverse("me-view")

    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK



@pytest.mark.django_db
def test_unauthenticated_user_cannot_access_Me_view(api_client):

    url = reverse("me-view")

    response = api_client.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED



@pytest.mark.django_db
def test_authenticated_user_can_access_Logout_view(api_client, user):

    api_client.force_authenticate(user=user)

    url = reverse("logout-view")

    response = api_client.post(url)

    assert response.status_code == status.HTTP_200_OK



@pytest.mark.django_db
def test_unauthenticated_user_cannot_access_Logout_view(api_client):

    url = reverse("logout-view")

    response = api_client.post(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED