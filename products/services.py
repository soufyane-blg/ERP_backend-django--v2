from rest_framework.exceptions import (
    ValidationError
)

from .models import Product

from .serializers import (
    ProductCreateUpdateSerializer,
)


def create_product(
    *,
    user,
    data,
):

    if user.organization is None:

        raise ValidationError(
            {
                "detail":
                "User does not belong "
                "to any organization."
            }
        )

    serializer = (
        ProductCreateUpdateSerializer(
            data=data
        )
    )

    serializer.is_valid(
        raise_exception=True
    )

    validated_data = (
        serializer.validated_data
    )

    product = Product.objects.create(

        name=validated_data["name"],

        description=validated_data.get(
            "description",
            "",
        ),

        price=validated_data["price"],

        stock=validated_data["stock"],

        category=validated_data.get(
            "category",
            "",
        ),

        organization=user.organization,
    )

    return product


def update_product(
    *,
    product,
    data,
):

    serializer = (
        ProductCreateUpdateSerializer(
            data=data,
            partial=True
        )
    )

    serializer.is_valid(
        raise_exception=True
    )

    validated_data = (
        serializer.validated_data
    )

    for field, value in (
        validated_data.items()
    ):

        setattr(
            product,
            field,
            value
        )

    product.save()

    return product


def delete_product(
    product,
):

    if product.orderitem_set.exists():

        raise ValidationError(
            {
                "detail":
                "Cannot delete a product "
                "used in orders."
            }
        )

    product.delete()