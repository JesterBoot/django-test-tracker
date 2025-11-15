from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from users.api.serializers import RefreshResponseSerializer
from users.services.dto.tokens import RefreshTokenDTO, RefreshTokenResponseDTO


@extend_schema(
    summary="Обновление access-токена по refresh-токену",
    request=inline_serializer(
        name="RefreshRequest",
        fields={"refresh": serializers.CharField()},
    ),
    responses={200: RefreshResponseSerializer},
)
class RefreshView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
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
