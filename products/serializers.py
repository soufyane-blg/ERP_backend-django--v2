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

    quantity = serializers.IntegerField(
        min_value=1
    )

    def validate_name(self, value):

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
        