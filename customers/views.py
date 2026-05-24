from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from .models import Customer

from .serializers import (
    CustomerReadSerializer,
)

from .services import (
    get_customers_for_organization,
    create_customer_for_organization,
    update_customer,
    delete_customer,
)

from accounts.permissions import (
    IsStaffOrReadOnly,
    HasSameOrganization,
)

from django_filters.rest_framework import (
    DjangoFilterBackend
)

from rest_framework.filters import (
    SearchFilter,
    OrderingFilter,
)

from .filters import CustomerFilter

class CustomerViewSet(viewsets.ModelViewSet):

    serializer_class = CustomerReadSerializer

    filter_backends = [
            DjangoFilterBackend,
            SearchFilter,
            OrderingFilter,
        ]

    filterset_class = CustomerFilter

    search_fields = [
            "name",
            "email",
        ]

    ordering_fields = [
            "created_at",
            "name",
        ]

    ordering = [
            "-created_at",
        ]

    def get_queryset(self):

        return get_customers_for_organization(
            self.request.user.organization
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

        customer = create_customer_for_organization(
            request.user.organization,
            request.data
        )

        serializer = self.get_serializer(customer)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):

        customer = self.get_object()

        updated_customer = update_customer(
            customer,
            request.data
        )

        serializer = self.get_serializer(
            updated_customer
        )

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):

        customer = self.get_object()

        delete_customer(customer)

        return Response(
            {"detail": "Customer deleted successfully."},
            status=204
        )
