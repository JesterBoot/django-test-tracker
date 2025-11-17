from uuid import UUID

from django.db.models import QuerySet

from workflows.models import Comment


def get_comment_by_id(comment_id: UUID) -> Comment | None:
    return (
        Comment.objects.select_related("author", "task")
        .only(
            "id",
            "task",
            "author",
            "text",
            "created_at",
            "updated_at",
        )
        .filter(id=comment_id)
        .first()
    )


def list_comments_for_task(
    task_id: UUID,
    limit: int = 200,
) -> QuerySet[Comment]:
    return (
        Comment.objects.select_related("author")
        .only(
            "id",
            "text",
            "author",
            "created_at",
            "updated_at",
        )
        .filter(task_id=task_id)
        .order_by("created_at")[:limit]
    )
