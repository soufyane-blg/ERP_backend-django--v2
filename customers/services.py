from django.db import IntegrityError
from rest_framework.exceptions import ValidationError

from .models import Customer
from .serializers import (
    CustomerCreateUpdateSerializer
)


def get_customers_for_organization(organization):
    return Customer.objects.filter(
        organization=organization
    )


def create_customer_for_organization(organization, data):

    serializer = CustomerCreateUpdateSerializer(
        data=data,
        context={
            "organization": organization
        }
    )

    serializer.is_valid(raise_exception=True)

    try:
        customer = Customer.objects.create(
            name=serializer.validated_data["name"],
            email=serializer.validated_data["email"],
            phone_number=serializer.validated_data.get(
                "phone_number",
                ""
            ),
            organization=organization
        )

        return customer

    except IntegrityError:
        raise ValidationError(
            "Customer already exists."
        )


def update_customer(customer, data):

    serializer = CustomerCreateUpdateSerializer(
        data=data,
        partial=True,
        context={
            "organization": customer.organization,
            "customer": customer
        }
    )

    serializer.is_valid(raise_exception=True)

    validated_data = serializer.validated_data

    customer.name = validated_data.get(
        "name",
        customer.name
    )

    customer.email = validated_data.get(
        "email",
        customer.email
    )

    customer.phone_number = validated_data.get(
        "phone_number",
        customer.phone_number
    )

    try:
        customer.save()
        return customer

    except IntegrityError:
        raise ValidationError(
            "Customer update failed."
        )


def delete_customer(customer):
    
    if customer.orders.exists():

        raise ValidationError(

            {

                "detail":

                "Cannot delete customer with existing orders."

            }

        )

    customer.delete()