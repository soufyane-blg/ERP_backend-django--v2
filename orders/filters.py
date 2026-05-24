import django_filters

from .models import Order


class OrderFilter(
    django_filters.FilterSet
):

    min_total = django_filters.NumberFilter(
        field_name="total",
        lookup_expr="gte",
    )

    max_total = django_filters.NumberFilter(
        field_name="total",
        lookup_expr="lte",
    )

    start_date = django_filters.DateFilter(
        field_name="order_date",
        lookup_expr="date__gte",
    )

    end_date = django_filters.DateFilter(
        field_name="order_date",
        lookup_expr="date__lte",
    )

    class Meta:

        model = Order

        fields = [
            "status",
        ]