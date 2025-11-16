from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

from users.exceptions.user_exceptions import (
    InvalidCredentialsError,
    UserAlreadyExistsError,
)


def custom_exception_handler(exc, context):
    if isinstance(exc, UserAlreadyExistsError):
        return Response(
            {
                "error": "user_already_exists",
                "message": str(exc),
            },
            status=status.HTTP_409_CONFLICT,
        )

    if isinstance(exc, InvalidCredentialsError):
        return Response(
            {
                "error": "invalid_credentials",
                "message": str(exc),
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )

    # передать управление стандартному DRF обработчику
    return exception_handler(exc, context)
