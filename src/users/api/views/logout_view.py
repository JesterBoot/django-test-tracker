from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.api.serializers import LogoutRequestSerializer
from users.services.dto.logout_dto import LogoutDTO
from users.services.user_logout import blacklist_refresh_token


@extend_schema(
    summary="Logout (инвалидация refresh-токена)",
    request=LogoutRequestSerializer,
    responses={204: OpenApiResponse(description="Успешный logout")},
)
class LogoutView(APIView):
    """
    Logout делает refresh-токен недействительным.
    Access-токен перестанет работать при истечении.
    """

    permission_classes = [IsAuthenticated]

    @staticmethod
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
