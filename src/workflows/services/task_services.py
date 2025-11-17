from uuid import UUID

from django.db import transaction

from users.models import User
from workflows.exceptions.task_exceptions import TaskNotFoundError, TaskPermissionDeniedError
from workflows.models import Task
from workflows.models.enums import TaskStatus
from workflows.selectors.task_selectors import get_task_by_id
from workflows.services.dto.task_dto import CreateTaskDTO, UpdateTaskDTO


@transaction.atomic
def create_task(data: CreateTaskDTO, *, user: User) -> Task:
    assignee = None
    if data["assignee_id"] is not None:
        assignee = User.objects.filter(id=data["assignee_id"]).first()

    task = Task.objects.create(
        title=data["title"],
        description=data.get("description", ""),
        created_by=user,
        assignee=assignee,
    )
    return task


def _ensure_can_edit(task: Task, user: User) -> None:
    allowed_user_ids = {task.created_by_id}
    if task.assignee_id:
        allowed_user_ids.add(task.assignee_id)

    if user.id not in allowed_user_ids:
        raise TaskPermissionDeniedError(
            "Редактировать задачу может только создатель или исполнитель."
        )


def _ensure_can_delete(task: Task, user: User) -> None:
    if task.created_by_id != user.id:
        raise TaskPermissionDeniedError("Удалить задачу может только создатель.")


@transaction.atomic
def update_task(task_id: UUID, data: UpdateTaskDTO, *, user: User) -> Task:
    task = get_task_by_id(task_id)
    if task is None:
        raise TaskNotFoundError

    _ensure_can_edit(task, user)

    if data.get("title") is not None:
        task.title = data["title"]

    if data.get("description") is not None:
        task.description = data["description"]

    if data.get("assignee_id") is not None:
        assignee = User.objects.filter(id=data["assignee_id"]).first()
        task.assignee = assignee

    if data.get("status") is not None:
        if data.get("status") not in TaskStatus.values:
            raise ValueError(f"Invalid status: {data.get('status')}")
        task.status = data.get("status")

    task.save(update_fields=["title", "description", "assignee", "status", "updated_at"])
    return task


@transaction.atomic
def delete_task(task_id: UUID, *, user: User) -> None:
    task = get_task_by_id(task_id)
    if task is None:
        raise TaskNotFoundError

    _ensure_can_delete(task, user)
    task.delete()


@transaction.atomic
def complete_task(task_id: UUID, *, user: User) -> Task:
    task = get_task_by_id(task_id)
    if task is None:
        raise TaskNotFoundError

    _ensure_can_edit(task, user)

    task.status = TaskStatus.DONE
    task.save(update_fields=["status", "updated_at"])
    return task
