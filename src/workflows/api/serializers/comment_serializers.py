from rest_framework import serializers

from workflows.models import Comment


class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "id",
            "author_id",
            "text",
            "created_at",
            "updated_at",
        ]


class CommentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "id",
            "task_id",
            "author_id",
            "text",
            "created_at",
            "updated_at",
        ]


class CommentCreateSerializer(serializers.Serializer):
    task_id = serializers.UUIDField()
    text = serializers.CharField()


class CommentUpdateSerializer(serializers.Serializer):
    text = serializers.CharField()
