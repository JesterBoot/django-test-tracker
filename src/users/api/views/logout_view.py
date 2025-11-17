from drf_spectacular.utils import OpenApiResponse, extend_schema, inline_serializer
from rest_framework import serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.services.dto.logout_dto import LogoutDTO
from users.services.user_logout import blacklist_refresh_token


logout_request_serializer = inline_serializer(
    name="LogoutRequest",
    fields={"refresh": serializers.CharField()},
)


@extend_schema(
    operation_id="auth_logout",
    tags=["Auth"],
    summary="Logout (инвалидация refresh-токена)",
    request=logout_request_serializer,
    responses={
        204: OpenApiResponse(description="Успешный logout"),
        400: OpenApiResponse(description="Refresh-токен не передан"),
        401: OpenApiResponse(description="Требуется аутентификация"),
    },
)
class LogoutView(APIView):
    """
    Logout делает refresh-токен недействительным.
    Access-токен перестанет работать при истечении.
    """

    permission_classes = [IsAuthenticated]

    @staticmethod
    @extend_schema(
        operation_id="auth_logout",
        tags=["Auth"],
        summary="Logout пользователя",
        request=logout_request_serializer,
        responses={
            204: OpenApiResponse(description="Успешный logout"),
            400: OpenApiResponse(description="Refresh токен не передан"),
        },
    )
    def post(request) -> Response:
        data: LogoutDTO = request.data

        if "refresh" not in data:
            return Response(
                {"error": "invalid_request", "message": "Missing 'refresh' token"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        blacklist_refresh_token(data)

        # По стандарту logout не возвращает тело
        return Response(status=status.HTTP_204_NO_CONTENT)
