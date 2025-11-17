from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

from users.exceptions.user_exceptions import (
    InvalidCredentialsError,
    UserAlreadyExistsError,
)
from workflows.exceptions.comment_exceptions import (
    CommentNotFoundError,
    CommentPermissionDeniedError,
)
from workflows.exceptions.task_exceptions import TaskNotFoundError, TaskPermissionDeniedError


def custom_exception_handler(exc, context):
    mapping = {
        UserAlreadyExistsError: ("user_already_exists", status.HTTP_409_CONFLICT),
        InvalidCredentialsError: ("invalid_credentials", status.HTTP_401_UNAUTHORIZED),
        TaskNotFoundError: ("task_not_found", status.HTTP_404_NOT_FOUND),
        TaskPermissionDeniedError: ("task_permission_denied", status.HTTP_403_FORBIDDEN),
        CommentNotFoundError: ("comment_not_found", status.HTTP_404_NOT_FOUND),
        CommentPermissionDeniedError: ("comment_permission_denied", status.HTTP_403_FORBIDDEN),
    }

    for exc_type, (error_code, http_status) in mapping.items():
        if isinstance(exc, exc_type):
            message = str(exc)
            if not message:
                if error_code == "task_not_found":
                    message = "Задача не найдена."
                elif error_code == "comment_not_found":
                    message = "Комментарий не найден."
            return Response({"error": error_code, "message": message}, status=http_status)

    return exception_handler(exc, context)
