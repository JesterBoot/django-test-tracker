from rest_framework.permissions import BasePermission

from workflows.models import Task


class IsTaskCreator(BasePermission):
    """
    Разрешает действие, только если пользователь — создатель задачи.
    """

    def has_object_permission(self, request, view, obj: Task) -> bool:
        return obj.created_by.id == request.user.id


class IsTaskCreatorOrAssignee(BasePermission):
    """
    Разрешает редактирование задачи:
    - создатель
    - назначенный исполнитель
    """

    def has_object_permission(self, request, view, obj: Task) -> bool:
        user_id = request.user.id
        return user_id in (obj.created_by.id, obj.assignee.id)
