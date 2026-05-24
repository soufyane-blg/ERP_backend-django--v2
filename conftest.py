# conftest.py

import pytest
from decimal import Decimal

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from accounts.models import Organization
from customers.models import Customer
from products.models import Product
from orders.models import Order, OrderItem


User = get_user_model()


# =========================
# API CLIENT
# =========================

@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def normal_authenticated_client(api_client, normal_user):
    api_client.force_authenticate(user=normal_user)
    return api_client


# =========================
# ORGANIZATIONS
# =========================

@pytest.fixture
def organization():
    return Organization.objects.create(
    name="Main Organization",
    email="main@test.com",
)


@pytest.fixture
def second_organization():
    return Organization.objects.create(
        name="Second Organization",
        email="second@test.com",
    )


# =========================
# USERS
# =========================

@pytest.fixture
def user(organization):
    return User.objects.create_user(
        username="staff@test.com",
        email="staff@test.com",
        password="StrongPass123",
        organization=organization,
        is_staff=True,
    )


@pytest.fixture
def normal_user(organization):
    return User.objects.create_user(
        username="user@test.com",
        email="user@test.com",
        password="StrongPass123",
        organization=organization,
        is_staff=False,
    )


@pytest.fixture
def second_user(second_organization):
    return User.objects.create_user(
        username="second@test.com",
        email="second@test.com",
        password="StrongPass123",
        organization=second_organization,
        is_staff=True,
    )

# =========================
# CUSTOMERS
# =========================

@pytest.fixture
def customer(organization):
    return Customer.objects.create(
        name="John Doe",
        email="john@example.com",
        phone_number="+123456789",
        organization=organization,
    )


@pytest.fixture
def second_customer(second_organization):
    return Customer.objects.create(
        name="Jane Doe",
        email="jane@example.com",
        phone_number="+987654321",
        organization=second_organization,
    )


# =========================
# PRODUCTS
# =========================

@pytest.fixture
def product(organization):
    return Product.objects.create(
        name="Laptop",
        description="Gaming Laptop",
        stock=10,
        price=Decimal("1000.00"),
        organization=organization,
    )


@pytest.fixture
def second_product(second_organization):
    return Product.objects.create(
        name="Phone",
        description="Smart Phone",
        stock=5,
        price=Decimal("500.00"),
        organization=second_organization,
    )


# =========================
# ORDERS
# =========================

@pytest.fixture
def order(organization, customer):
    return Order.objects.create(
        customer=customer,
        organization=organization,
        status="pending",
        total=Decimal("2000.00"),
    )


@pytest.fixture
def shipped_order(organization, customer):
    return Order.objects.create(
        customer=customer,
        organization=organization,
        status="shipped",
        total=Decimal("1000.00"),
    )


@pytest.fixture
def delivered_order(organization, customer):
    return Order.objects.create(
        customer=customer,
        organization=organization,
        status="delivered",
        total=Decimal("1000.00"),
    )


@pytest.fixture
def canceled_order(organization, customer):
    return Order.objects.create(
        customer=customer,
        organization=organization,
        status="canceled",
        total=Decimal("1000.00"),
    )


# =========================
# ORDER ITEMS
# =========================

@pytest.fixture
def order_item(order, product):
    return OrderItem.objects.create(
        order=order,
        product=product,
        quantity=2,
        price=product.price,
    )