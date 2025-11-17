from typing import TypedDict
from uuid import UUID


class CreateTaskDTO(TypedDict):
    title: str
    description: str
    assignee_id: UUID | None


class UpdateTaskDTO(TypedDict):
    title: str | None
    description: str | None
    assignee_id: UUID | None
    status: str | None


class TaskDTO(TypedDict):
    id: UUID
    title: str
    description: str
    status: str
    created_by: UUID
    assignee: UUID | None
    created_at: str
    updated_at: str
