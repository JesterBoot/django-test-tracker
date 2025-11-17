from rest_framework.permissions import BasePermission

from workflows.models import Comment


class IsCommentAuthor(BasePermission):
    """
    Разрешает редактировать или удалять комментарий только автору.
    """

    def has_object_permission(self, request, view, obj: Comment) -> bool:
        return obj.author.id == request.user.id
