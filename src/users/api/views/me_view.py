from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.api.serializers import MeResponseSerializer
from users.selectors.user_selectors import get_user_me_dto


@extend_schema(
    summary="Информация о текущем пользователе",
    responses={200: MeResponseSerializer},
)
class MeView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request) -> Response:
        user = request.user
        dto = get_user_me_dto(user)
        return Response(dto, status=status.HTTP_200_OK)
