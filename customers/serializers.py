from rest_framework import serializers
from .models import Customer


class CustomerCreateUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(
        max_length=250,
        required=True
    )

    email = serializers.EmailField(
        required=True
    )

    phone_number = serializers.CharField(
        max_length=20,
        required=False,
        allow_blank=True
    )
    
    def validate_name(self, value):

        value = value.strip()

        if len(value) < 2:
            raise serializers.ValidationError(
                "Customer name is too short."
            )

        return value
    
    def validate_email(self, value):
        organization = self.context["organization"]
        customer = self.context.get("customer")
        
        value = value.lower().strip()
        
        queryset = Customer.objects.filter(
            organization=organization,
            email=value
        )

        if customer:
            queryset = queryset.exclude(pk=customer.pk)

        if queryset.exists():
            raise serializers.ValidationError(
                "A customer with this email already exists."
            )

        return value

    def validate_phone_number(self, value):
        
        value = value.strip()
        
        if not value:
            return value

        organization = self.context["organization"]
        customer = self.context.get("customer")

        queryset = Customer.objects.filter(
            organization=organization,
            phone_number=value
        )

        if customer:
            queryset = queryset.exclude(pk=customer.pk)

        if queryset.exists():
            raise serializers.ValidationError(
                "A customer with this phone number already exists."
            )

        return value


class CustomerReadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = "__all__"