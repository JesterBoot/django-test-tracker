from drf_spectacular.utils import OpenApiResponse, extend_schema, inline_serializer
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from core.throttling import RefreshTokenRateThrottle
from users.api.serializers import RefreshResponseSerializer
from users.services.dto.tokens import RefreshTokenDTO, RefreshTokenResponseDTO


refresh_request_serializer = inline_serializer(
    name="RefreshRequest",
    fields={"refresh": serializers.CharField()},
)


@extend_schema(
    operation_id="auth_refresh",
    tags=["Auth"],
    summary="Обновление access-токена по refresh",
    request=refresh_request_serializer,
    responses={
        200: RefreshResponseSerializer,
        400: OpenApiResponse(description="Refresh-токен не передан"),
        401: OpenApiResponse(description="Невалидный refresh-токен"),
        429: OpenApiResponse(description="Слишком много запросов обновления токена"),
    },
)
class RefreshView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [RefreshTokenRateThrottle]

    @staticmethod
    @extend_schema(
        operation_id="auth_refresh",
        tags=["Auth"],
        summary="Обновление токена",
        request=refresh_request_serializer,
        responses={
            200: RefreshResponseSerializer,
            400: OpenApiResponse(description="Отсутствует refresh токен"),
            401: OpenApiResponse(description="Неверный refresh токен"),
        },
    )
    def post(request) -> Response:
        data: RefreshTokenDTO = request.data

        if "refresh" not in data:
            return Response(
                {"error": "invalid_request", "message": "Missing 'refresh' token"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            token = RefreshToken(data["refresh"])  # type: ignore[arg-type]
            access = str(token.access_token)
        except TokenError:
            return Response(
                {"error": "invalid_refresh_token", "message": "Refresh token is invalid"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        response_data: RefreshTokenResponseDTO = {
            "access": access,
        }

        return Response(response_data, status=status.HTTP_200_OK)
