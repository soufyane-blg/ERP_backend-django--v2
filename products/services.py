from rest_framework.exceptions import ValidationError

from .models import Product

from .serializers import (
    ProductCreateUpdateSerializer,
)


def create_product(*, user, data):

    if user.organization is None:
        raise ValidationError(
            {
                "detail":
                "User does not belong to any organization."
            }
        )

    serializer = ProductCreateUpdateSerializer(
        data=data
    )

    serializer.is_valid(raise_exception=True)

    product = Product.objects.create(
        name=serializer.validated_data["name"],
        description=serializer.validated_data.get(
            "description",
            ""
        ),
        stock=serializer.validated_data["quantity"],
        organization=user.organization
    )

    return product


def update_product(*, product, data):

    serializer = ProductCreateUpdateSerializer(
        data=data,
        partial=True
    )

    serializer.is_valid(raise_exception=True)

    validated_data = serializer.validated_data

    if "name" in validated_data:
        product.name = validated_data["name"]

    if "description" in validated_data:
        product.description = validated_data[
            "description"
        ]

    if "quantity" in validated_data:
        product.stock = validated_data[
            "quantity"
        ]

    product.save()

    return product


def delete_product(product):

    if product.order_items.exists():

        raise ValidationError(
            {
                "detail":
                "Cannot delete a product used in orders."
            }
        )

    product.delete()