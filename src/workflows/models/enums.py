from django.db import models


class TaskStatus(models.TextChoices):
    TODO = "todo", "To Do"
    IN_PROGRESS = "in_progress", "In Progress"
    DONE = "done", "Done"
