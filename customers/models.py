from django.db import models
from accounts.models import Organization


class Customer(models.Model):
    name = models.CharField(max_length=250)

    email = models.EmailField()

    phone_number = models.CharField(
        max_length=20,
        blank=True
    )

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="customers"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

        constraints = [
            models.UniqueConstraint(
                fields=["organization", "email"],
                name="unique_customer_email_per_organization"
            ),

            models.UniqueConstraint(
                fields=["organization", "phone_number"],
                name="unique_customer_phone_per_organization"
            )
        ]

    def __str__(self):
        return self.name

