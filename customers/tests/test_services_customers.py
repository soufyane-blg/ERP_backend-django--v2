# customers/tests/test_services.py

import pytest
from rest_framework.exceptions import ValidationError

from customers.models import Customer
from customers.services import (
    get_customers_for_organization,
    create_customer_for_organization,
    update_customer,
    delete_customer,
)


@pytest.mark.django_db
def test_get_customers_for_organization(
    organization,
    second_organization,
    customer,
    second_customer
):
    customers = get_customers_for_organization(
        organization
    )

    assert customer in customers
    assert second_customer not in customers


@pytest.mark.django_db
def test_create_customer_for_organization(
    organization
):
    data = {
        "name": "New Customer",
        "email": "new@example.com",
        "phone_number": "+111111111"
    }

    customer = create_customer_for_organization(
        organization,
        data
    )

    assert customer.name == data["name"]
    assert customer.organization == organization


@pytest.mark.django_db
def test_create_customer_duplicate_email(
    organization,
    customer
):
    data = {
        "name": "Duplicate",
        "email": customer.email,
        "phone_number": "+111111111"
    }

    with pytest.raises(ValidationError):
        create_customer_for_organization(
            organization,
            data
        )


@pytest.mark.django_db
def test_update_customer(customer):

    data = {
        "name": "Updated Name"
    }

    updated_customer = update_customer(
        customer,
        data
    )

    assert updated_customer.name == "Updated Name"


@pytest.mark.django_db
def test_update_customer_invalid_email(customer):

    data = {
        "email": "invalid-email"
    }

    with pytest.raises(ValidationError):
        update_customer(customer, data)


@pytest.mark.django_db
def test_delete_customer(customer):

    delete_customer(customer)

    assert not Customer.objects.filter(
        id=customer.id
    ).exists()