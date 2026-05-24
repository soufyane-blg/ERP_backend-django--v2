# tests/test_order_services.py

import pytest
from decimal import Decimal

from rest_framework.exceptions import ValidationError

from orders.models import (
    Order,
    OrderItem,
)

from orders.services import (
    create_order,
    change_order_status,
)

from products.models import Product


@pytest.mark.django_db
class TestCreateOrderService:

    def test_create_order_success(
        self,
        user,
        organization,
        product,
    ):

        data = {
            "customer": "John Doe",
            "items": [
                {
                    "product": product.id,
                    "quantity": 2,
                }
            ]
        }

        order = create_order(
            data=data,
            organization=organization,
            user=user,
        )

        product.refresh_from_db()

        assert Order.objects.count() == 1

        assert OrderItem.objects.count() == 1

        assert order.total == Decimal("2000.00")

        assert product.stock == 8

    def test_create_order_empty_customer(
        self,
        user,
        organization,
        product,
    ):

        data = {
            "customer": "   ",
            "items": [
                {
                    "product": product.id,
                    "quantity": 1,
                }
            ]
        }

        with pytest.raises(ValidationError):

            create_order(
                data=data,
                organization=organization,
                user=user,
            )

    def test_create_order_empty_items(
        self,
        user,
        organization,
    ):

        data = {
            "customer": "John",
            "items": [],
        }

        with pytest.raises(ValidationError):

            create_order(
                data=data,
                organization=organization,
                user=user,
            )

    def test_create_order_invalid_quantity(
        self,
        user,
        organization,
        product,
    ):

        data = {
            "customer": "John",
            "items": [
                {
                    "product": product.id,
                    "quantity": 0,
                }
            ]
        }

        with pytest.raises(ValidationError):

            create_order(
                data=data,
                organization=organization,
                user=user,
            )

    def test_create_order_out_of_stock(
        self,
        user,
        organization,
        product,
    ):

        product.stock = 0

        product.save()

        data = {
            "customer": "John",
            "items": [
                {
                    "product": product.id,
                    "quantity": 1,
                }
            ]
        }

        with pytest.raises(ValidationError):

            create_order(
                data=data,
                organization=organization,
                user=user,
            )

    def test_create_order_not_enough_stock(
        self,
        user,
        organization,
        product,
    ):

        data = {
            "customer": "John",
            "items": [
                {
                    "product": product.id,
                    "quantity": 50,
                }
            ]
        }

        with pytest.raises(ValidationError):

            create_order(
                data=data,
                organization=organization,
                user=user,
            )

    def test_create_order_product_from_other_organization(
        self,
        user,
        organization,
        second_organization,
    ):

        foreign_product = Product.objects.create(
            name="Foreign Product",
            price=Decimal("500.00"),
            stock=10,
            organization=second_organization,
        )

        data = {
            "customer": "John",
            "items": [
                {
                    "product": foreign_product.id,
                    "quantity": 1,
                }
            ]
        }

        with pytest.raises(ValidationError):

            create_order(
                data=data,
                organization=organization,
                user=user,
            )


@pytest.mark.django_db
class TestChangeOrderStatus:

    def test_change_pending_to_shipped(
        self,
        order,
    ):

        updated_order = change_order_status(
            order,
            "shipped",
        )

        assert updated_order.status == "shipped"

    def test_change_shipped_to_delivered(
        self,
        shipped_order,
    ):

        updated_order = change_order_status(
            shipped_order,
            "delivered",
        )

        assert updated_order.status == "delivered"

    def test_invalid_transition(
        self,
        order,
    ):

        with pytest.raises(ValidationError):

            change_order_status(
                order,
                "delivered",
            )

    def test_invalid_status(
        self,
        order,
    ):

        with pytest.raises(ValidationError):

            change_order_status(
                order,
                "unknown",
            )

    def test_cannot_modify_delivered_order(
        self,
        delivered_order,
    ):

        with pytest.raises(ValidationError):

            change_order_status(
                delivered_order,
                "pending",
            )

    def test_cannot_modify_canceled_order(
        self,
        canceled_order,
    ):

        with pytest.raises(ValidationError):

            change_order_status(
                canceled_order,
                "pending",
            )