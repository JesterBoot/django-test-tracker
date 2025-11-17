from django.urls import path

from workflows.api.views import (
    CommentDetailView,
    CommentListCreateView,
    TaskDetailView,
    TaskListCreateView,
)


urlpatterns = [
    # Tasks
    path("tasks/", TaskListCreateView.as_view(), name="task-list"),
    path("tasks/<uuid:task_id>/", TaskDetailView.as_view(), name="task-detail"),
    # Comments
    path("tasks/<uuid:task_id>/comments/", CommentListCreateView.as_view(), name="comment-list"),
    path("comments/<uuid:comment_id>/", CommentDetailView.as_view(), name="comment-detail"),
]
