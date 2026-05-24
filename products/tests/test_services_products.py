import pytest
from rest_framework.exceptions import ValidationError

from products.models import Product
from products.services import (
    create_product,
    update_product,
    delete_product,
)


@pytest.mark.django_db
def test_create_product(user):

    data = {
        "name": "Keyboard",
        "description": "Mechanical keyboard",
        "stock": 15,
        "price": 99.99,
    }

    product = create_product(
        user=user,
        data=data
    )

    assert product.name == data["name"]
    assert product.stock == data["stock"]
    assert product.organization == (
        user.organization
    )


# احذف هذا الاختبار إذا organization غير nullable
# لأنه لم يعد ممكنًا إنشاء user بدون organization


@pytest.mark.django_db
def test_create_product_invalid_stock(user):

    data = {
        "name": "Keyboard",
        "description": "Mechanical keyboard",
        "stock": -5,
        "price": 99.99,
    }

    with pytest.raises(ValidationError):
        create_product(
            user=user,
            data=data
        )


@pytest.mark.django_db
def test_update_product(product):

    data = {
        "name": "Updated Laptop",
        "stock": 20,
        "price": 1200.00,
    }

    updated_product = update_product(
        product=product,
        data=data
    )

    assert updated_product.name == (
        "Updated Laptop"
    )

    assert updated_product.stock == 20
    assert updated_product.price == 1200.00


@pytest.mark.django_db
def test_update_product_invalid_stock(
    product
):
    data = {
        "stock": -10
    }

    with pytest.raises(ValidationError):
        update_product(
            product=product,
            data=data
        )


@pytest.mark.django_db
def test_delete_product(product):

    delete_product(product)

    assert not Product.objects.filter(
        id=product.id
    ).exists()