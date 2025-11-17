import uuid

from django.conf import settings
from django.db import models

from workflows.models.enums import TaskStatus


class Task(models.Model):
    id: uuid.UUID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title: str = models.CharField(max_length=255)
    description: str = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=TaskStatus.choices, default=TaskStatus.TODO)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="created_tasks"
    )
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_tasks",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tasks"
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        ordering = ("-created_at",)
        indexes = [
            models.Index(
                fields=("status", "assignee"),
                name="task_status_assignee_idx",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.title} ({self.status})"
