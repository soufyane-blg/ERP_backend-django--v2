from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError

from .models import Order

from .serializers import (
    OrderReadSerializer,
)

from .services import (
    create_order,
    change_order_status
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

from .filters import OrderFilter


class OrderViewSet(viewsets.ModelViewSet):

    serializer_class = OrderReadSerializer

    filter_backends = [
    DjangoFilterBackend,
    SearchFilter,
    OrderingFilter,
    ]

    filterset_class = OrderFilter

    search_fields = [
        "customer__name",
    ]

    ordering_fields = [
        "order_date",
        "total",
    ]

    ordering = [
        "-order_date",
    ]

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

        elif self.action in ["update", "partial_update"]:
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

        elif self.action == "change_status":
            permission_classes = [
                IsAuthenticated,
                IsStaffOrReadOnly,
                HasSameOrganization,
            ]

        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def get_queryset(self):

        user = self.request.user

        return (
            Order.objects
            .filter(
                organization=user.organization
            )
            .select_related("customer")
            .prefetch_related("items__product")
            .order_by("-order_date")
        )

    def create(self, request, *args, **kwargs):

        order = create_order(
            data=request.data,
            organization=request.user.organization,
            user=request.user
        )

        serializer = self.get_serializer(order)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=["patch"])
    def change_status(self, request, pk=None):

        order = self.get_object()

        new_status = request.data.get("status")

        if not new_status:
            raise ValidationError(
                {"status": "This field is required"}
            )

        order = change_order_status(
            order,
            new_status
        )

        serializer = self.get_serializer(order)

        return Response(serializer.data)