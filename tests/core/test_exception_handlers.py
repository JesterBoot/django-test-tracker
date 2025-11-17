from rest_framework import status

from core.exception_handlers import custom_exception_handler
from workflows.exceptions.comment_exceptions import CommentNotFoundError
from workflows.exceptions.task_exceptions import TaskNotFoundError


def test_custom_exception_handler_default_messages():
    resp = custom_exception_handler(TaskNotFoundError(""), context={})
    assert resp.status_code == status.HTTP_404_NOT_FOUND
    assert resp.data["message"] == "Задача не найдена."

    resp2 = custom_exception_handler(CommentNotFoundError(""), context={})
    assert resp2.status_code == status.HTTP_404_NOT_FOUND
    assert resp2.data["message"] == "Комментарий не найден."


def test_custom_exception_handler_passthrough_returns_none():
    class UnknownError(Exception):
        pass

    assert custom_exception_handler(UnknownError(""), context={}) is None
