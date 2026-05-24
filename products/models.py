from django.db import models

from accounts.models import (
    Organization
)


class Product(models.Model):

    name = models.CharField(
        max_length=250
    )

    description = models.TextField(
        blank=True
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    stock = models.PositiveIntegerField(
        default=1
    )

    category = models.CharField(
        max_length=100,
        blank=True
    )

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="products"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        ordering = ["-created_at"]

        indexes = [

            models.Index(
                fields=["organization"]
            ),

            models.Index(
                fields=["category"]
            ),

            models.Index(
                fields=["price"]
            ),
        ]

    def __str__(self):

        return self.name