from rest_framework import serializers

from workflows.models import Task
from workflows.models.enums import TaskStatus


class TaskDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "created_by_id",
            "assignee_id",
            "created_at",
            "updated_at",
        ]


class TaskListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "status",
            "assignee_id",
            "created_at",
        ]


class TaskCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(required=False, allow_blank=True)
    assignee_id = serializers.UUIDField(required=False, allow_null=True)


class TaskUpdateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255, required=False)
    description = serializers.CharField(required=False, allow_blank=True)
    assignee_id = serializers.UUIDField(required=False, allow_null=True)
    status = serializers.ChoiceField(
        choices=TaskStatus.choices,
        required=False,
    )
