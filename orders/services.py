# services.py

from decimal import Decimal

from django.db import transaction
from rest_framework.exceptions import ValidationError

from customers.models import Customer
from products.models import Product

from .models import Order, OrderItem
from .serializers import OrderCreateSerializer


VALID_TRANSITIONS = {
    "pending": ["shipped", "canceled"],
    "shipped": ["delivered"],
    "delivered": [],
    "canceled": [],
}


@transaction.atomic
def create_order(data, organization, user):

    serializer = OrderCreateSerializer(
        data=data,
        context={"request": user}
    )

    serializer.is_valid(raise_exception=True)

    validated_data = serializer.validated_data

    customer_name = validated_data["customer"].strip()

    items_data = validated_data["items"]

    if not customer_name:
        raise ValidationError(
            {
                "customer":
                "Customer name cannot be empty."
            }
        )

    if user.organization != organization:
        raise ValidationError(
            {
                "detail":
                "Invalid organization."
            }
        )

    customer, _ = Customer.objects.get_or_create(
        name=customer_name,
        organization=organization
    )

    order = Order.objects.create(
        customer=customer,
        organization=organization,
    )

    product_ids = [
        item["product"].id
        for item in items_data
    ]

    products = {
        product.id: product
        for product in Product.objects
        .select_for_update()
        .filter(
            id__in=product_ids,
            organization=organization
        )
    }

    total = Decimal("0.00")

    order_items = []

    for item_data in items_data:

        product = item_data["product"]

        quantity = item_data["quantity"]

        if quantity <= 0:
            raise ValidationError(
                {
                    "quantity":
                    "Quantity must be greater than 0."
                }
            )

        if product.id not in products:
            raise ValidationError(
                {
                    "detail":
                    f"Product {product.id} "
                    f"does not belong to "
                    f"your organization."
                }
            )

        locked_product = products[product.id]

        if locked_product.quantity <= 0:
            raise ValidationError(
                {
                    "detail":
                    f"{locked_product.name} "
                    f"is out of stock."
                }
            )

        if quantity > locked_product.quantity:
            raise ValidationError(
                {
                    "detail":
                    f"Not enough stock for "
                    f"{locked_product.name}."
                }
            )

        locked_product.quantity -= quantity

        order_items.append(
            OrderItem(
                order=order,
                product=locked_product,
                quantity=quantity,
                price=locked_product.price
            )
        )

        total += (
            locked_product.price * quantity
        )

    if total <= Decimal("0.00"):
        raise ValidationError(
            {
                "detail":
                "Order total must be greater than zero."
            }
        )

    Product.objects.bulk_update(
        products.values(),
        ["quantity"]
    )

    OrderItem.objects.bulk_create(order_items)

    order.total = total

    order.save()

    return order


def change_order_status(order, new_status):

    new_status = new_status.lower().strip()

    if new_status not in VALID_TRANSITIONS:
        raise ValidationError(
            {
                "status":
                "Invalid status."
            }
        )

    if order.status in ["delivered", "canceled"]:
        raise ValidationError(
            {
                "detail":
                "Finalized orders cannot be modified."
            }
        )

    allowed_statuses = VALID_TRANSITIONS[
        order.status
    ]

    if new_status not in allowed_statuses:
        raise ValidationError(
            {
                "detail":
                f"Cannot change status from "
                f"{order.status} to "
                f"{new_status}."
            }
        )

    order.status = new_status

    order.save()

    return order