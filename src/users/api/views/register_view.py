from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from users.api.serializers import RegisterResponseSerializer, RegisterSerializer
from users.api.tokens import generate_user_tokens
from users.services.dto.register import RegisterUserDTO, RegisterUserResponseDTO
from users.services.user_services import register_user


@extend_schema(
    operation_id="auth_register",
    tags=["Auth"],
    summary="Регистрация нового пользователя",
    request=RegisterSerializer,
    responses={
        201: RegisterResponseSerializer,
        400: OpenApiResponse(description="Ошибка валидации данных"),
        409: OpenApiResponse(description="Пользователь с таким email уже существует"),
    },
)
class RegisterView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request) -> Response:
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data: RegisterUserDTO = {
            "email": serializer.validated_data["email"],
            "password": serializer.validated_data["password"],
        }

        user = register_user(data)
        tokens = generate_user_tokens(user)

        response_data: RegisterUserResponseDTO = {
            "user_id": str(user.id),
            "email": user.email,
            "tokens": tokens,
        }

        return Response(response_data, status=status.HTTP_201_CREATED)
