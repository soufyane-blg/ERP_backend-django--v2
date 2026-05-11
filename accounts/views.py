from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .serializers import RegisterSerializer, LoginSerializer
from .services import (
    register_user,
    login_service,
    logout_service,
    refresh_tokens_service,
    get_current_user
)


class RegisterView(APIView):

    def post(self, request):

        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = register_user(**serializer.validated_data)

        return Response(result, status=status.HTTP_201_CREATED)


class LoginView(APIView):

    def post(self, request):

        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = login_service(**serializer.validated_data)

        response = Response({
            "user_id": result["user_id"],
            "username": result["username"],
            "access": result["access"],
        })

        response.set_cookie(
            key="refresh_token",
            value=result["refresh"],
            httponly=True,
            secure=True,
            samesite="Lax",
            max_age=7 * 24 * 60 * 60,
        )

        return response


class RefreshView(APIView):

    def post(self, request):

        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return Response(
                {"detail": "Refresh token missing"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        result = refresh_tokens_service(refresh_token)

        response = Response({
            "access": result["access"]
        })

        response.set_cookie(
            key="refresh_token",
            value=result["refresh"],
            httponly=True,
            secure=True,
            samesite="Lax",
            max_age=7 * 24 * 60 * 60,
        )

        return response


class MeView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        data = get_current_user(request.user)

        return Response(data)


class LogoutView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        refresh_token = request.COOKIES.get("refresh_token")

        if refresh_token:
            logout_service(refresh_token)

        response = Response(
            {"detail": "Logged out successfully"},
            status=status.HTTP_200_OK
        )

        response.delete_cookie("refresh_token")

        return response