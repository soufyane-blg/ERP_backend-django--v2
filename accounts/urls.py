from django.urls import path

from .views import (
    RegisterView,
    LoginView,
    RefreshView,
    MeView,
    LogoutView,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="registration-view"),
    path("login/", LoginView.as_view(), name="login"),
    path("refresh/", RefreshView.as_view(), name="refresh-view"),
    path("me/", MeView.as_view(), name="me-view"),
    path("logout/", LogoutView.as_view(), name="logout-view"),
]
