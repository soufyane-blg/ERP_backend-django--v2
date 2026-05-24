import pytest
from django.urls import reverse
from rest_framework import status

from customers.models import Customer


@pytest.mark.django_db
def test_authentication_required(api_client):

    response = api_client.get(
        reverse("customer-list")
    )

    assert response.status_code == (
        status.HTTP_401_UNAUTHORIZED
    )


@pytest.mark.django_db
def test_list_customers(
    authenticated_client,
    customer
):
    response = authenticated_client.get(
        reverse("customer-list")
    )

    assert response.status_code == (
        status.HTTP_200_OK
    )

    assert len(response.data["results"]) == 1
    assert response.data["results"][0]["name"] == customer.name


@pytest.mark.django_db
def test_user_only_sees_own_organization_customers(
    authenticated_client,
    customer,
    second_customer
):
    response = authenticated_client.get(
        reverse("customer-list")
    )

    customer_ids = [
        item["id"]
        for item in response.data["results"]
    ]

    assert customer.id in customer_ids
    assert second_customer.id not in customer_ids


@pytest.mark.django_db
def test_create_customer(
    authenticated_client,
    organization
):
    payload = {
        "name": "Created Customer",
        "email": "created@example.com",
        "phone_number": "+111111111"
    }

    response = authenticated_client.post(
        reverse("customer-list"),
        payload,
        format="json"
    )

    assert response.status_code == (
        status.HTTP_201_CREATED
    )

    customer = Customer.objects.get(
        id=response.data["id"]
    )

    assert customer.name == payload["name"]
    assert customer.organization == organization


@pytest.mark.django_db
def test_create_customer_invalid_email(
    authenticated_client
):
    payload = {
        "name": "Invalid",
        "email": "invalid-email",
        "phone_number": "+111111111"
    }

    response = authenticated_client.post(
        reverse("customer-list"),
        payload,
        format="json"
    )

    assert response.status_code == (
        status.HTTP_400_BAD_REQUEST
    )


@pytest.mark.django_db
def test_non_staff_cannot_create_customer(
    normal_authenticated_client
):
    payload = {
        "name": "Created Customer",
        "email": "created@example.com",
        "phone_number": "+111111111"
    }

    response = normal_authenticated_client.post(
        reverse("customer-list"),
        payload,
        format="json"
    )

    assert response.status_code == (
        status.HTTP_403_FORBIDDEN
    )


@pytest.mark.django_db
def test_update_customer(
    authenticated_client,
    customer
):
    payload = {
        "name": "Updated Customer"
    }

    response = authenticated_client.patch(
        reverse(
            "customer-detail",
            args=[customer.id]
        ),
        payload,
        format="json"
    )

    assert response.status_code == (
        status.HTTP_200_OK
    )

    customer.refresh_from_db()

    assert customer.name == (
        "Updated Customer"
    )


@pytest.mark.django_db
def test_delete_customer(
    authenticated_client,
    customer
):
    response = authenticated_client.delete(
        reverse(
            "customer-detail",
            args=[customer.id]
        )
    )

    assert response.status_code == (
        status.HTTP_204_NO_CONTENT
    )

    assert not Customer.objects.filter(
        id=customer.id
    ).exists()


@pytest.mark.django_db
def test_user_cannot_access_other_organization_customer(
    authenticated_client,
    second_customer
):
    response = authenticated_client.get(
        reverse(
            "customer-detail",
            args=[second_customer.id]
        )
    )

    assert response.status_code in [
        status.HTTP_404_NOT_FOUND,
        status.HTTP_403_FORBIDDEN
    ]