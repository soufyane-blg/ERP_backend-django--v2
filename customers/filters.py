import django_filters

from .models import Customer


class CustomerFilter(
    django_filters.FilterSet
):

    joined_after = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr="date__gte",
    )

    joined_before = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr="date__lte",
    )

    class Meta:

        model = Customer

        fields = []