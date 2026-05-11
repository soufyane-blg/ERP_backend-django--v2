from django.db import models
from django.contrib.auth.models import AbstractUser


class Organization(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class User(AbstractUser):
    email = models.EmailField(unique=True)
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="users"
    )
    
    role = models.CharField(
    max_length=20,
    choices=[
        ("admin", "Admin"),
        ("staff", "Staff"),
    ],
    default="staff"
)


    def __str__(self):
        return self.email