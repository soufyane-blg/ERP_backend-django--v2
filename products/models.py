from django.db import models
from accounts.models import Organization




class Product(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(blank= True)
    stock = models.IntegerField(default=1)
    organization = models.ForeignKey(Organization,on_delete=models.CASCADE, related_name="products")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name