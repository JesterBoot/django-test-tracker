from typing import TypedDict
from uuid import UUID


class CreateCommentDTO(TypedDict):
    task_id: UUID
    text: str


class UpdateCommentDTO(TypedDict):
    text: str


class CommentDTO(TypedDict):
    id: UUID
    task_id: UUID
    author_id: UUID
    text: str
    created_at: str
    updated_at: str
