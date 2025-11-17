from uuid import UUID

from django.db import transaction

from users.models import User
from workflows.exceptions.comment_exceptions import (
    CommentNotFoundError,
    CommentPermissionDeniedError,
)
from workflows.exceptions.task_exceptions import TaskNotFoundError
from workflows.models import Comment
from workflows.selectors.comment_selectors import (
    get_comment_by_id,
)
from workflows.selectors.task_selectors import get_task_by_id
from workflows.services.dto.comment_dto import CreateCommentDTO, UpdateCommentDTO


@transaction.atomic
def create_comment(data: CreateCommentDTO, *, user: User) -> Comment:
    task = get_task_by_id(data["task_id"])

    if task is None:
        raise TaskNotFoundError("Задача не найдена.")

    comment = Comment.objects.create(
        task=task,
        author=user,
        text=data["text"],
    )

    return comment


def _ensure_can_edit(comment: Comment, user: User) -> None:
    if comment.author.id != user.id:
        raise CommentPermissionDeniedError("Редактировать комментарий может только автор.")


def _ensure_can_delete(comment: Comment, user: User) -> None:
    if comment.author.id != user.id:
        raise CommentPermissionDeniedError("Удалить комментарий может только автор.")


@transaction.atomic
def update_comment(comment_id: UUID, data: UpdateCommentDTO, *, user: User) -> Comment:
    comment = get_comment_by_id(comment_id)
    if comment is None:
        raise CommentNotFoundError("Комментарий не найден.")

    _ensure_can_edit(comment, user)

    comment.text = data["text"]
    comment.save(update_fields=["text", "updated_at"])

    return comment


@transaction.atomic
def delete_comment(comment_id: UUID, *, user: User) -> None:
    comment = get_comment_by_id(comment_id)
    if comment is None:
        raise CommentNotFoundError("Комментарий не найден.")

    _ensure_can_delete(comment, user)

    comment.delete()
