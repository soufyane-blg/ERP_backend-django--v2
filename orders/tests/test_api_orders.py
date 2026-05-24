import pytest

from rest_framework import status
from rest_framework.test import APIClient

from orders.models import Order


@pytest.mark.django_db
class TestOrderViews:

    def test_list_orders(
        self,
        user,
        order,
    ):

        client = APIClient()

        client.force_authenticate(
            user=user
        )

        response = client.get(
            "/api/orders/"
        )

        assert response.status_code == (
            status.HTTP_200_OK
        )

    def test_create_order(
        self,
        user,
        organization,
        product,
    ):

        payload = {
            "customer": "John Doe",
            "items": [
                {
                    "product": product.id,
                    "quantity": 2,
                }
            ]
        }

        client = APIClient()

        client.force_authenticate(
            user=user
        )

        response = client.post(
            "/api/orders/",
            payload,
            format="json",
        )

        assert response.status_code == (
            status.HTTP_201_CREATED
        )

        assert Order.objects.count() == 1

    def test_create_order_unauthenticated(
        self,
        product,
    ):

        payload = {
            "customer": "John Doe",
            "items": [
                {
                    "product": product.id,
                    "quantity": 1,
                }
            ]
        }

        client = APIClient()

        response = client.post(
            "/api/orders/",
            payload,
            format="json",
        )

        assert response.status_code == (
            status.HTTP_401_UNAUTHORIZED
        )

    def test_create_order_non_staff_user(
        self,
        normal_user,
        product,
    ):

        payload = {
            "customer": "John Doe",
            "items": [
                {
                    "product": product.id,
                    "quantity": 1,
                }
            ]
        }

        client = APIClient()

        client.force_authenticate(
            user=normal_user
        )

        response = client.post(
            "/api/orders/",
            payload,
            format="json",
        )

        assert response.status_code == (
            status.HTTP_403_FORBIDDEN
        )

    def test_change_status(
        self,
        user,
        order,
    ):

        client = APIClient()

        client.force_authenticate(
            user=user
        )

        response = client.patch(
            f"/api/orders/{order.id}/change_status/",
            {"status": "shipped"},
            format="json",
        )

        assert response.status_code == (
            status.HTTP_200_OK
        )

        order.refresh_from_db()

        assert order.status == "shipped"

    def test_change_status_without_status(
        self,
        user,
        order,
    ):

        client = APIClient()

        client.force_authenticate(
            user=user
        )

        response = client.patch(
            f"/api/orders/{order.id}/change_status/",
            {},
            format="json",
        )

        assert response.status_code == (
            status.HTTP_400_BAD_REQUEST
        )

    def test_user_cannot_access_other_organization_order(
        self,
        second_user,
        order,
    ):

        client = APIClient()

        client.force_authenticate(
            user=second_user
        )

        response = client.get(
            f"/api/orders/{order.id}/"
        )

        assert response.status_code in [
            status.HTTP_403_FORBIDDEN,
            status.HTTP_404_NOT_FOUND,
        ]