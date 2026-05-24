from rest_framework import serializers

from .models import Product


class ProductCreateUpdateSerializer(
    serializers.Serializer
):

    name = serializers.CharField(
        max_length=250
    )

    description = serializers.CharField(
        required=False,
        allow_blank=True
    )

    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0
    )

    stock = serializers.IntegerField(
        min_value=0
    )

    category = serializers.CharField(
        max_length=100,
        required=False,
        allow_blank=True
    )

    def validate_name(
        self,
        value,
    ):

        value = value.strip()

        if len(value) < 2:

            raise serializers.ValidationError(
                "Product name is too short."
            )

        return value


class ProductReadSerializer(
    serializers.ModelSerializer
):

    class Meta:

        model = Product

        fields = "__all__"
        