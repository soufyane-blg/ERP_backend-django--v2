from .views import ProductslistCreateView, ProductDetailView
from django.urls import path

urlpatterns = [
    path("products/", ProductslistCreateView.as_view(), name="products-list-create"),
    path("products/<int:pk>/", ProductDetailView.as_view(), name="product-detail"),
]