from uuid import UUID

from django.db.models import QuerySet

from workflows.models import Task
from workflows.models.enums import TaskStatus


def get_task_by_id(task_id: UUID) -> Task | None:
    return (
        Task.objects.only(
            "id",
            "title",
            "description",
            "status",
            "created_by",
            "assignee",
            "created_at",
            "updated_at",
        )
        .filter(id=task_id)
        .first()
    )


def list_tasks_filtered(
    *,
    status: str | None = None,
    assignee_id: UUID | None = None,
    limit: int = 200,
) -> QuerySet[Task]:
    qs = Task.objects.select_related("created_by", "assignee")

    if status:
        if status not in TaskStatus.values:
            raise ValueError(f"Invalid status '{status}'")
        qs = qs.filter(status=status)

    if assignee_id:
        qs = qs.filter(assignee_id=assignee_id)

    return qs.order_by("-created_at")[:limit]
