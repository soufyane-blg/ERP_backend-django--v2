from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Product

from .serializers import (
    ProductReadSerializer,
)

from .services import (
    create_product,
    update_product,
    delete_product,
)

from accounts.permissions import (
    IsStaffOrReadOnly,
    HasSameOrganization,
)


class ProductViewSet(viewsets.ModelViewSet):

    serializer_class = ProductReadSerializer

    def get_queryset(self):

        return (
            Product.objects
            .filter(
                organization=self.request.user.organization
            )
            .order_by("-created_at")
        )

    def get_permissions(self):

        if self.action in ["list", "retrieve"]:
            permission_classes = [
                IsAuthenticated,
                HasSameOrganization,
            ]

        elif self.action == "create":
            permission_classes = [
                IsAuthenticated,
                IsStaffOrReadOnly,
            ]

        elif self.action in [
            "update",
            "partial_update",
        ]:
            permission_classes = [
                IsAuthenticated,
                IsStaffOrReadOnly,
                HasSameOrganization,
            ]

        elif self.action == "destroy":
            permission_classes = [
                IsAuthenticated,
                IsStaffOrReadOnly,
            ]

        else:
            permission_classes = [IsAuthenticated]

        return [
            permission()
            for permission in permission_classes
        ]

    def create(self, request, *args, **kwargs):

        product = create_product(
            user=request.user,
            data=request.data
        )

        serializer = self.get_serializer(product)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):

        product = self.get_object()

        updated_product = update_product(
            product=product,
            data=request.data,
        )

        serializer = self.get_serializer(
            updated_product
        )

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):

        product = self.get_object()

        delete_product(product)

        return Response(
            {
                "detail":
                "Product deleted successfully."
            },
            status=status.HTTP_204_NO_CONTENT
        )