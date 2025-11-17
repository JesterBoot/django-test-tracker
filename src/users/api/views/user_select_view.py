from drf_spectacular.utils import OpenApiParameter, extend_schema, OpenApiResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.api.serializers.user_short_serializer import UserShortSerializer
from users.selectors.user_list_selectors import select_users


@extend_schema(
    operation_id="users_select",
    tags=["Users"],
    summary="Получить список пользователей для выбора исполнителя задачи",
    parameters=[
        OpenApiParameter(
            name="q",
            type=str,
            required=False,
            description="Поиск по email (частичное совпадение)",
        ),
        OpenApiParameter(
            name="limit",
            type=int,
            required=False,
            description="Максимальное количество пользователей (по умолчанию 20)",
        ),
    ],
    responses={
        200: UserShortSerializer,
        401: OpenApiResponse(description="Требуется аутентификация"),
    },
)
class UserSelectView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        q = request.query_params.get("q")
        limit_raw = request.query_params.get("limit")

        try:
            limit = int(limit_raw) if limit_raw is not None else 20
        except ValueError:
            limit = 20

        users = select_users(
            q=q,
            limit=limit,
            exclude_user_id=request.user.id,
        )

        return Response(UserShortSerializer(users, many=True).data)
