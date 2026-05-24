# serializers.py

from rest_framework import serializers
from .models import Order, OrderItem
from products.models import Product


class OrderItemCreateSerializer(
    serializers.Serializer
):

    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all()
    )

    quantity = serializers.IntegerField(
        min_value=1
    )

    def validate_product(
        self,
        product,
    ):

        user = self.context.get("user")

        if (
            user
            and product.organization
            != user.organization
        ):

            raise serializers.ValidationError(
                "This product does not belong "
                "to your organization."
            )

        return product
    



class OrderCreateSerializer(serializers.Serializer):
    customer = serializers.CharField(max_length=255)
    items = OrderItemCreateSerializer(many=True)

    def validate_items(self, value):

        if not value:
            raise serializers.ValidationError(
                "Order must contain at least one item."
            )

        return value

class OrderItemReadSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name")

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product",
            "product_name",
            "quantity",
            "price",
        ]


class OrderReadSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source="customer.name")
    items = OrderItemReadSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "customer_name",
            "status",
            "total",
            "order_date",
            "items",
        ]