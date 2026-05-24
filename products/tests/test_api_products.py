# products/tests/test_api.py

import pytest
from django.urls import reverse
from rest_framework import status

from products.models import Product


@pytest.mark.django_db
def test_authentication_required(api_client):

    response = api_client.get(
        reverse("product-list")
    )

    assert response.status_code == (
        status.HTTP_401_UNAUTHORIZED
    )


@pytest.mark.django_db
def test_list_products(
    authenticated_client,
    product
):
    response = authenticated_client.get(
        reverse("product-list")
    )

    assert response.status_code == (
        status.HTTP_200_OK
    )

    results = response.data["results"]

    assert len(results) == 1

    assert results[0]["name"] == (
        product.name
    )


@pytest.mark.django_db
def test_user_only_sees_own_organization_products(
    authenticated_client,
    product,
    second_product
):
    response = authenticated_client.get(
        reverse("product-list")
    )

    results = response.data["results"]

    product_ids = [
        item["id"]
        for item in results
    ]

    assert product.id in product_ids

    assert second_product.id not in product_ids


@pytest.mark.django_db
def test_create_product(
    authenticated_client
):
    payload = {
        "name": "Monitor",
        "description": "4K Monitor",
        "stock": 7,
        "price": 500.00,
    }

    response = authenticated_client.post(
        reverse("product-list"),
        payload,
        format="json"
    )

    assert response.status_code == (
        status.HTTP_201_CREATED
    )

    product = Product.objects.get(
        id=response.data["id"]
    )

    assert product.name == payload["name"]

    assert product.stock == (
        payload["stock"]
    )


@pytest.mark.django_db
def test_create_product_invalid_stock(
    authenticated_client
):
    payload = {
        "name": "Monitor",
        "description": "4K Monitor",
        "stock": -1,
        "price": 500.00,
    }

    response = authenticated_client.post(
        reverse("product-list"),
        payload,
        format="json"
    )

    assert response.status_code == (
        status.HTTP_400_BAD_REQUEST
    )


@pytest.mark.django_db
def test_non_staff_cannot_create_product(
    normal_authenticated_client
):
    payload = {
        "name": "Monitor",
        "description": "4K Monitor",
        "stock": 7,
        "price": 500.00,
    }

    response = (
        normal_authenticated_client.post(
            reverse("product-list"),
            payload,
            format="json"
        )
    )

    assert response.status_code == (
        status.HTTP_403_FORBIDDEN
    )


@pytest.mark.django_db
def test_update_product(
    authenticated_client,
    product
):
    payload = {
        "name": "Updated Product",
        "stock": 50,
    }

    response = authenticated_client.patch(
        reverse(
            "product-detail",
            args=[product.id]
        ),
        payload,
        format="json"
    )

    assert response.status_code == (
        status.HTTP_200_OK
    )

    product.refresh_from_db()

    assert product.name == (
        "Updated Product"
    )

    assert product.stock == 50


@pytest.mark.django_db
def test_delete_product(
    authenticated_client,
    product
):
    response = authenticated_client.delete(
        reverse(
            "product-detail",
            args=[product.id]
        )
    )

    assert response.status_code == (
        status.HTTP_204_NO_CONTENT
    )

    assert not Product.objects.filter(
        id=product.id
    ).exists()


@pytest.mark.django_db
def test_user_cannot_access_other_organization_product(
    authenticated_client,
    second_product
):
    response = authenticated_client.get(
        reverse(
            "product-detail",
            args=[second_product.id]
        )
    )

    assert response.status_code in [
        status.HTTP_404_NOT_FOUND,
        status.HTTP_403_FORBIDDEN,
    ]