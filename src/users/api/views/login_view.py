from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from core.throttling import LoginRateThrottle
from users.api.serializers import LoginResponseSerializer, LoginSerializer
from users.api.tokens import generate_user_tokens
from users.services.dto.login import LoginUserDTO, LoginUserResponseDTO
from users.services.user_services import authenticate_user


class LoginView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [LoginRateThrottle]

    @staticmethod
    @extend_schema(
        operation_id="auth_login",
        tags=["Auth"],
        summary="Авторизация пользователя",
        request=LoginSerializer,
        responses={
            200: LoginResponseSerializer,
            400: OpenApiResponse(description="Ошибка валидации данных"),
            401: OpenApiResponse(description="Неверный email или пароль"),
            429: OpenApiResponse(description="Слишком много попыток входа"),
        },
    )
    def post(request) -> Response:
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data: LoginUserDTO = {
            "email": serializer.validated_data["email"],
            "password": serializer.validated_data["password"],
        }

        # InvalidCredentialsError при ошибке
        user = authenticate_user(data)
        tokens = generate_user_tokens(user)

        response_data: LoginUserResponseDTO = {
            "user_id": str(user.id),
            "email": user.email,
            "tokens": tokens,
        }

        return Response(response_data, status=status.HTTP_200_OK)
