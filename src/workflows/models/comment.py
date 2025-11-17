import uuid

from django.conf import settings
from django.db import models


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    task = models.ForeignKey("workflows.Task", on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="task_comments"
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "comments"
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ("created_at",)
        indexes = [
            models.Index(fields=("task", "created_at"), name="comment_task_created_idx"),
        ]

    def __str__(self) -> str:
        return f"Комментарий от {self.author}, задача - {self.task}"
